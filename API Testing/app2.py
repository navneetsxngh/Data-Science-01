from flask import Flask, request, render_template, redirect, jsonify
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

with open("models/logistic.pkl", "rb") as file:
    model = pickle.load(file)

@app.route('/predict', methods = ['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = np.array(data['input']).reshape(1, -1)
        prediction = model.predict(input_data)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)