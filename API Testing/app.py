from flask import Flask, request, render_template, redirect
import numpy as np
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

scaler = pickle.load(open('models/scaler.pkl', 'rb'))
linearmodel = pickle.load(open('models/LinearRegression.pkl', 'rb'))
encoding = pickle.load(open('models/encoder.pkl', 'rb'))

# Mapping dictionaries based on your training data
sex_mapping = {'female': 0, 'male': 1}
smoker_mapping = {'no': 0, 'yes': 1}
region_mapping = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == "POST":
        age = float(request.form.get('age'))
        sex = request.form.get('sex')
        bmi = float(request.form.get('bmi'))
        children = float(request.form.get('children'))
        smoker = request.form.get('smoker')
        region = request.form.get('region')

        # Manually encode categorical variables using the mappings
        sex_encoded = sex_mapping.get(sex.lower(), 0)
        smoker_encoded = smoker_mapping.get(smoker.lower(), 0)
        region_encoded = region_mapping.get(region.lower(), 0)
        
        # Create feature array with encoded values
        features = [[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]]
        
        # Scale the features
        scaling = scaler.transform(features)
        
        # Make prediction
        prediction = linearmodel.predict(scaling)

        return render_template('predict.html', results = round(prediction[0], 2))
    else:
        return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')