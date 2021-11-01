import pickle

from flask import Flask
from flask import request
from flask import jsonify

model_file = 'RandomForest_maxdepth10_nestimators200.bin'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

app = Flask('batalactamases')

@app.route('/predict', methods=['POST'])
def predict():
    molecule = request.get_json()

    molecule = molecule.to

    y_pred = model.predict_proba(molecule)[0, 1]
    active = y_pred >= 0.5

    result = {
        'Activity against betalactamase probability': float(y_pred),
        'Active': bool(active)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)