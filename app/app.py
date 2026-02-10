from flask import Flask, render_template, request
import joblib
import re

app = Flask(__name__)

# Load model and vectorizer
model = joblib.load('models/phishing_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    email_text = request.form['email'].strip()

    # Check if input is a valid email address
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_text):
        return render_template('index.html', prediction="⚠️ Please enter a valid email address!", email=email_text)

    # Predict phishing or legitimate
    vect = vectorizer.transform([email_text])
    prediction = model.predict(vect)[0]

    result = "🚨 Phishing Email" if prediction == 1 else "✅ Legitimate Email"
    return render_template('index.html', prediction=result, email=email_text)

if __name__ == '__main__':
    app.run(debug=True)
