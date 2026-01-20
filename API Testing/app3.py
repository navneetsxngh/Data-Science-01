from flask import Flask, request, render_template, redirect, jsonify
import numpy as np
import pandas as pd
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

app = Flask(__name__)

with open("models/logistic.pkl", "rb") as file:
    model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():

    data = {
        'RowNumber': request.form.get('RowNumber'),
        'CustomerId': request.form.get('CustomerId'),
        'CreditScore': request.form.get('CreditScore'),
        'Geography': request.form.get('Geography'),
        'Gender': request.form.get('Gender'),
        'Age': request.form.get('Age'),
        'Tenure': request.form.get('Tenure'),
        'Balance': request.form.get('Balance'),
        'NumOfProducts': request.form.get('NumofProducts'),
        'HasCrCard': request.form.get('HasCrCard'),
        'IsActiveMember': request.form.get('IsActiveMember'),
        'EstimatedSalary': request.form.get('EstimatedSalary')
    }

    df = pd.DataFrame([data])

    num_cols = [
        'RowNumber', 'CustomerId', 'CreditScore', 'Age',
        'Tenure', 'Balance', 'NumOfProducts',
        'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
    ]
    df[num_cols] = df[num_cols].astype(float)

    df['Geography'] = df['Geography'].map({
        'France': 0,
        'Spain': 1,
        'Germany': 2
    })

    df['Gender'] = df['Gender'].map({
        'Male': 1,
        'Female': 0
    })

    # if df.isna().any().any():
    #     return jsonify({
    #         "error": "Invalid input detected",
    #         "nan_columns": df.isna().sum().to_dict()
    #     }), 400

    prediction = model.predict(df)

    return jsonify({
        "prediction": int(prediction[0])
    })


if __name__ == '__main__':
    app.run(debug=True)