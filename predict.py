# Imports
import pickle

from flask import Flask
from flask import request
from flask import jsonify
from padelpy import padeldescriptor
import json
import pandas as pd

# Load the best ML model
model_file = 'RandomForest_maxdepth10_nestimators200.bin'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

# Create a flask app
app = Flask('batalactamase')

# Create a post method to receive requests
@app.route('/predict', methods=['POST'])
def predict():
    # Obtain information of the molecule to be predicted as a json file
    molecule = request.get_json()

    molecule = json.loads(molecule)

    # Convert json file to a dataframe
    molecule_df= pd.DataFrame(molecule)

    # Export .smi file to be used by padelpy
    molecule_df.to_csv('molecule_test.smi', sep='\t', index=False, header=False)

    # Load .smi file and calculate CDK fingerprint from the molecule 
    # to be tested 
    fingerprint_outfile = 'CDK_example_testing.csv'

    fingerprint_descriptorfile = 'Fingerprinter.xml'

    padeldescriptor(mol_dir='molecule_test.smi', 
                    d_file=fingerprint_outfile,
                    descriptortypes= fingerprint_descriptorfile,
                    detectaromaticity=True,
                    standardizenitro=True,
                    standardizetautomers=True,
                    threads=2,
                    removesalt=True,
                    log=False,
                    fingerprints=True)

    # Load CDK fingerprint results and names of the low variance 
    # features of CDK obtained in training 
    cdk_molecule_df = pd.read_csv("CDK_example_testing.csv") 

    low_var_feat_names = pd.read_csv("low_var_feat_names.csv")

    # Filter low variance features of CDK fingerprint from the molecule 
    # to be tested 
    cdk_low_var = cdk_molecule_df.drop('Name', axis=1)
    cdk_low_var = cdk_molecule_df[low_var_feat_names["Descriptor_Name"].values]

    # Make predictions with the best model 
    y_pred = model.predict_proba(cdk_low_var)[0, 1]
    active = y_pred >= 0.5

    # Save results 
    result = {
        'Activity against Beta-lactamase AmpC probability': float(y_pred),
        'Active': bool(active)
    }

    # Convert results to a json file for posting them into a web service
    return jsonify(result)

# Run the app in the main 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)