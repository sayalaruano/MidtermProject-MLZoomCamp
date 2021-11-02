#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
import requests

# Parameters 
url = 'http://localhost:9696/predict'

molecule_id = 'CHEMBL1796'

canonical_smile = 'Cc1sc(cc1\C(=C\C(=O)C(=O)O)\O)c2ccccc2'

# Create a dataframe with name and canonical smile of the molecule to 
# be predicted 
molecule = {"Canonical_smile": canonical_smile, 
            "Chembl_id": molecule_id}

molecule_df = pd.DataFrame(molecule, index=[0])

# Convert dataframe to json
molecule_json = molecule_df.to_json(orient="records")

# Create a post to the web service of activity prediction 
response = requests.post(url, json=molecule_json).json()
print(response)

# Print steps that we need to follow according to the results 
if response['Active'] == True:
    print('Molecule %s is active against Beta-lactamase AmpC' % molecule_id)
else:
    print('Molecule %s is not active against Beta-lactamase AmpC' % molecule_id)
