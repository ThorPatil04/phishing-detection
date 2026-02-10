import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
df = pd.read_csv('phishing_site_urls.csv')

# Convert labels
df['Label'] = df['Label'].map({'bad': 1, 'good': 0}).fillna(df['Label'])

# Feature extraction
def extract_features(url):
    return [
        len(url),
        url.count('.'),
        1 if 'https' in url else 0,
        1 if '@' in url else 0,
        1 if '-' in url else 0,
        1 if re.search(r'login|verify|bank|secure|update', url.lower()) else 0
    ]

X = df['URL'].astype(str).apply(extract_features).tolist()
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

# Save model
with open('phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)
