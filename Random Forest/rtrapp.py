from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

with open("rtr.pkl", "rb") as file1:
    model = pickle.load(file1)

with open("scaler.pkl", 'rb') as file2:
    scaler = pickle.load(file2)

@app.route('/predict', methods=['POST'])
def predict():

    data = {
        'age': float(request.form.get('age')),
        'sex': request.form.get('sex').lower(),
        'bmi': float(request.form.get('bmi')),
        'children': float(request.form.get('children')),
        'smoker': request.form.get('smoker').lower(),
        'region': request.form.get('region').lower(),
    }

    df = pd.DataFrame([data])

    # Encoding
    df['sex'] = df['sex'].map({'male': 1, 'female': 0})
    df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})
    df['region'] = df['region'].map({
        'southwest': 3,
        'southeast': 2,
        'northwest': 1,
        'northeast': 0
    })

    df_scaled = scaler.transform(df)

    prediction = model.predict(df_scaled)

    return jsonify({
        "prediction": float(prediction[0])
    })

if __name__ == '__main__':
    app.run(debug=True)