#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
from padelpy import padeldescriptor
import requests

# Parameters 
url = 'http://localhost:9696/predict'

molecule_id = 'CHEMBL179256'

canonical_smile = 'OC(=O)c1ccc2c(c1)nc(c3ccc(O)cc3F)n2C4CCCCC4'

# Create a dataframe with name and canonical smile of the molecule to 
# be predicted 
molecule = {"Canonical_smile": canonical_smile, 
            "Chembl_id": molecule_id}

molecule_df = pd.DataFrame(molecule, index=[0])

# Export .smi file to be used by padelpy
molecule_df.to_csv('molecule_test.smi', sep='\t', index=False, header=False)

# Load .smi file and calculate CDK fingerprint from the molecule 
# to be tested 
fingerprint_outfile = 'CDK_example_testing.csv'

fingerprint_descriptorfile = 'Data/MolFingerprints/Fingerprinter.xml'

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

# Convert dataframe to json
cdk_molecule_json = cdk_low_var.to_json(orient="records")

# Create a post to the web service of activity prediction 
response = requests.post(url, json=cdk_molecule_json).json()
print(response)

# Print steps that we need to follow according to the results 
if response['Active'] == True:
    print('Molecule %s is active against Beta-lactamase AmpC' % molecule_id)
else:
    print('Molecule %s is not active against Beta-lactamase AmpC' % molecule_id)
