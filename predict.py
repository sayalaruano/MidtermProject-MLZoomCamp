# Imports
import pickle

from flask import Flask
from flask import request
from flask import jsonify
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

    # Make predictions with the best model 
    y_pred = model.predict_proba(molecule_df)[0, 1]
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