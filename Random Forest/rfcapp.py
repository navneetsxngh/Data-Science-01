from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

with open("rf.pkl", "rb") as file:
    model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    data = {
        'User ID': float(request.form.get('User Id')),
        'Gender': request.form.get('Gender'),
        'Age': float(request.form.get('Age')),
        'EstimatedSalary': float(request.form.get('EstimatedSalary'))
    }

    df = pd.DataFrame([data])

    df['Gender'] = df['Gender'].map({
        'Male': 1,
        'Female': 0
    })

    prediction = model.predict(df)

    return jsonify({
        "prediction": int(prediction[0])
    })

if __name__ == '__main__':
    app.run(debug=True)
