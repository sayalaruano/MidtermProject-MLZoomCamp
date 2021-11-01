#!/usr/bin/env python
# coding: utf-8

# Imports
## Data manipulation and EDA
import zipfile
import pandas as pd
import numpy as np
import pickle

## Molecular descriptors calculation 
from padelpy import padeldescriptor

## Machine learning models
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

# Parameters
maxdepth = 10
nestimators = 200
n_splits = 5
output_file = f'RandomForest_maxdepth{maxdepth}_nestimators{nestimators}.bin'

# Data preparation
## Load feature matrix - CDK fingerprint (dataset with the best performance)
cdk_fingerprint = pd.read_csv('Data/ML_model_training/CDK_training.csv')

## Load y target variable - pchembl values
pchembl_values = pd.read_csv('Data/ML_model_training/pchembl_values.csv')

## Function to remove low variance features
def remove_low_variance(input_data, threshold=0.1):
    selection = VarianceThreshold(threshold)
    selection.fit(input_data)
    return input_data[input_data.columns[selection.get_support(indices=True)]]

## Obtain feature matrix with low variance features 
cdk_low_var = cdk_fingerprint.drop('Name', axis=1)
cdk_low_var = remove_low_variance(cdk_low_var, threshold=(.8*(1-.8)))

## Data split 
X_train, X_test, y_train, y_test = train_test_split(cdk_low_var, pchembl_values, 
                                                    test_size=0.2, random_state=42)

# Training 
print(f'Training the model')

rf = RandomForestClassifier(max_depth=maxdepth, n_estimators=nestimators, n_jobs=-1, 
                            random_state=10).fit(X_train, y_train)

# Validation

print(f'Doing validation')
print(f'ROC AUC is used as performance metric')

cv_scores = cross_val_score(rf, X_train, y_train, cv=n_splits, scoring="roc_auc")

print('Validation results:')
print(f'RandomForest with max_depth={maxdepth} and n_estimators={nestimators}: \
    {np.mean(cv_scores):.2f} +- {np.std(cv_scores):.2f}')

# Predicting values with RF model on test dataset 
print(f'Doing evaluation on test dataset')
y_test_pred = rf.predict(X_test)

## Calculate performance metrics
roc_auc_test = roc_auc_score(y_test, y_test_pred)

acc_test = accuracy_score(y_test, y_test_pred)

prec_test = precision_score(y_test, y_test_pred)

recall_test = recall_score(y_test, y_test_pred)

f1score_test = f1_score(y_test, y_test_pred)

## Print metrics values 
print(f'Testing results:')
metrics_names = ["ROC_AUC", "Accuracy", "Precision", "Recall", "F1 score"]
metrics_values = [roc_auc_test, acc_test, prec_test, recall_test, f1score_test]

metrics = dict(zip(metrics_names, metrics_values))

headers = ('Metric', 'Value')
spaces = ('----------', '----------')

head_spaces = [headers, spaces]

for metric, value in head_spaces:
    print(f'{metric:>10s} {value:>10s}')

for metric, value in metrics.items():
    print(f'{metric:>10s} {value:>10.2f}')

# Save the model

with open(output_file, "wb") as f_out:
    pickle.dump(rf, f_out)

print(f'The model is saved to {output_file}')
