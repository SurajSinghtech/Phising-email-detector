SOC Threat Intelligence System

Email Phishing and Attachment Analysis Platform

Overview

This project is a security-focused application that detects phishing emails and analyzes suspicious file attachments. It follows a layered approach similar to real-world security systems by combining machine learning with static file analysis.

Features
Email Phishing Detection
Machine learning-based classification
Uses text vectorization techniques
Predicts whether an email is phishing or legitimate
Attachment Analysis
File upload support
SHA256 hash generation
File extension analysis
Double extension detection (e.g., .pdf.exe)
Suspicious keyword detection
File size-based risk evaluation
Threat Scoring
Assigns a risk score from 0 to 100
Classifies threat levels as Low, Medium, or High
Web Interface
Dashboard for email and file analysis
Displays results clearly with risk indicators
Machine Learning Model
Algorithm: Linear Support Vector Classifier (LinearSVC)
Feature Extraction: TF-IDF Vectorization
Evaluation Metrics:
Accuracy
Precision
Recall
F1 Score
Model Performance
Metric	Value
Accuracy	XX%
Precision	XX
Recall	XX
F1 Score	XX

Replace the values above with your actual results.

Tech Stack
Frontend: HTML, CSS
Backend: Flask (Python)
Machine Learning: scikit-learn
Data Handling: pandas, numpy
NLP: NLTK
Utilities: joblib, hashlib
Project Structure

phishing_email_detector/

app/
app.py
templates/
index.html
scripts/
train_model.py
models/
phishing_model.pkl
vectorizer.pkl
uploads/
data/
README.md
How to Run
Clone the repository
git clone https://github.com/YOUR_USERNAME/phishing-email-detector.git
Navigate to the project folder
cd phishing-email-detector
Activate virtual environment
venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Run the application
python app\app.py
Open in browser
http://127.0.0.1:5000
Testing

Example email input:
security-update@paypal-loginverify.net

Example file names for testing:
invoice_update.exe
payment_receipt.pdf.exe
urgent_password_reset.txt

Key Concepts
Machine learning classification
Natural language processing
Static file analysis
Risk scoring systems
Web application development using Flask
Future Improvements
URL phishing detection
Confusion matrix visualization
Scan history logging
Cloud deployment
Advanced model improvements
Author

Your Name

Disclaimer

This project does not execute real malware.
All attachment analysis is based on safe static techniques.
