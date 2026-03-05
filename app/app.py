from flask import Flask, render_template, request
import joblib
import os
import hashlib
import re


app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


try:
    model = joblib.load("models/phishing_model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
except:
    model = None
    vectorizer = None


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return render_template("index.html", prediction="Model not loaded")

    email_text = request.form["email"]

  
    email_text = email_text.strip()

    vect = vectorizer.transform([email_text])

    prediction = model.predict(vect)[0]

    if prediction == 1:
        result = "🚨 Phishing Email Detected"
    else:
        result = "✅ Legitimate Email"

    return render_template("index.html", prediction=result)


@app.route("/analyze_attachment", methods=["POST"])
def analyze_attachment():

    if "attachment" not in request.files:
        return render_template("index.html")

    file = request.files["attachment"]

    if file.filename == "":
        return render_template("index.html")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    file_size = os.path.getsize(filepath)
    file_extension = os.path.splitext(file.filename)[1].lower()

    
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    file_hash = sha256_hash.hexdigest()

    risk_score = 0

    suspicious_extensions = [".exe", ".bat", ".scr", ".js", ".vbs"]

    if file_extension in suspicious_extensions:
        risk_score += 50

   
    if file_size > 5 * 1024 * 1024:
        risk_score += 20

    
    if len(file.filename.split(".")) > 2:
        risk_score += 20

    suspicious_keywords = ["invoice", "update", "urgent", "password", "verify"]
    for word in suspicious_keywords:
        if re.search(word, file.filename.lower()):
            risk_score += 10
            break

   
    if risk_score > 100:
        risk_score = 100

   
    if risk_score >= 70:
        threat_level = "HIGH"
    elif risk_score >= 40:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    return render_template(
        "index.html",
        attachment_result={
            "filename": file.filename,
            "hash": file_hash,
            "size": file_size,
            "risk": risk_score,
            "level": threat_level
        }
    )


if __name__ == "__main__":
    app.run(debug=True)