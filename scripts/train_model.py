# scripts/train_model.py
import pandas as pd
import joblib
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report

# --- Ensure models folder exists ---
os.makedirs('models', exist_ok=True)

# --- Step 1: Dataset ---
data = {
    'email': [
        # 🧨 Phishing
        'support@paypal-login.com',
        'security@netflix-update.com',
        'mailer@angelbroking.in',
        'noreply@bank-secureverify.com',
        'info@account-lock-alert.com',
        'update@appleid-reset.com',
        'verify@your-amazon-payment.com',
        'support@icicibank-verify.net',
        'alert@user-verification.com',
        'helpdesk@secure-login-update.org',
        'suraj123@phising-gmail.com',
        'bitch11@experian.com',

        # ✅ Legitimate
        'support@paypal.com',
        'info@netflix.com',
        'noreply@angelbroking.com',
        'support@amazon.in',
        'updates@apple.com',
        'alerts@icicibank.com',
        'no-reply@google.com',
        'service@hdfcbank.com',
        'contact@swiggy.in',
        'support@zomato.com',
        'surajhaibhadwa@gmail.com',
    ],
    'label': [
        1,1,1,1,1,1,1,1,1,1,1,1,  # Phishing
        0,0,0,0,0,0,0,0,0,0,0     # Legit
    ]
}

df = pd.DataFrame(data)

# --- Step 2: Known Safe Domains ---
SAFE_DOMAINS = [
    'paypal.com', 'netflix.com', 'angelbroking.com', 'amazon.in',
    'apple.com', 'icicibank.com', 'google.com', 'hdfcbank.com',
    'swiggy.in', 'zomato.com', 'gmail.com'
]

# --- Step 3: Feature Extraction Function ---
def extract_features(email):
    email = email.lower().strip()
    parts = email.split('@')
    username = parts[0]
    domain = parts[1] if len(parts) > 1 else ''

    # Custom features
    features = {
        "domain": domain,
        "username": username,
        "has_numbers": bool(re.search(r'\d', username)),
        "has_specials": bool(re.search(r'[_\-\.]', username)),
        "has_suspicious_word": any(w in email for w in ["verify", "secure", "update", "alert", "reset", "login"]),
        "is_safe_domain": domain in SAFE_DOMAINS,
        "is_suspicious_tld": any(domain.endswith(tld) for tld in ['.net', '.org', '.ru', '.biz', '.top', '.xyz']),
        "contains_bad_word": any(w in username for w in ["bitch", "hack", "test", "fake", "spam"]),
    }

    # Combine all into a single string
    feature_text = " ".join([
        f"domain:{domain}",
        f"user:{username}",
        f"num:{features['has_numbers']}",
        f"special:{features['has_specials']}",
        f"susp:{features['has_suspicious_word']}",
        f"safe:{features['is_safe_domain']}",
        f"tld:{features['is_suspicious_tld']}",
        f"bad:{features['contains_bad_word']}"
    ])

    return feature_text

df['features'] = df['email'].apply(extract_features)

# --- Step 4: Split ---
X_train, X_test, y_train, y_test = train_test_split(
    df['features'], df['label'], test_size=0.3, random_state=42, stratify=df['label']
)

# --- Step 5: Character-level TF-IDF Vectorization ---
# Better for short email strings
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 6))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# --- Step 6: Train Model ---
model = MultinomialNB(alpha=0.1)
model.fit(X_train_vec, y_train)

# --- Step 7: Evaluate ---
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy * 100:.2f} %")
print(classification_report(y_test, y_pred, target_names=["Legit", "Phishing"]))

# --- Step 8: Save Model ---
joblib.dump(model, 'models/phishing_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')
print("💾 Model and vectorizer saved successfully!")
