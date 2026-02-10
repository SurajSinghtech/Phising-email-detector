# scripts/data_preprocessing.py

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

# Download necessary nltk data
nltk.download('stopwords')

# Initialize stemmer
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# ✅ Step 1: Load dataset
print("📥 Loading dataset...")

# For now, let's create a small sample dataset manually
data = {
    'text': [
        'Congratulations! You have won a $1000 Walmart gift card. Click here to claim now!',
        'Your Netflix subscription has been renewed successfully.',
        'Urgent! Update your bank details immediately to avoid suspension.',
        'Hey, are we still on for lunch tomorrow?',
        'Get cheap meds now!!! No prescription required.'
    ],
    'label': [1, 0, 1, 0, 1]  # 1 = phishing, 0 = legitimate
}

df = pd.DataFrame(data)
print("✅ Dataset created successfully!")
print(df.head())

# ✅ Step 2: Clean the text
print("\n🧹 Cleaning text data...")

def preprocess_text(text):
    words = text.lower().split()
    words = [stemmer.stem(word) for word in words if word.isalpha() and word not in stop_words]
    return " ".join(words)

df['clean_text'] = df['text'].apply(preprocess_text)
print("✅ Text cleaned successfully!")

# ✅ Step 3: Convert to TF-IDF vectors
print("\n🔠 Converting text to numerical features...")
vectorizer = TfidfVectorizer(max_features=500)
X = vectorizer.fit_transform(df['clean_text']).toarray()

# ✅ Step 4: Save vectorizer for later use
os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
print("✅ TF-IDF vectorizer saved in models/tfidf_vectorizer.pkl")

print("\n🎉 Preprocessing complete!")

