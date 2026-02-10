from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

model = pickle.load(open('phishing_model.pkl', 'rb'))

def extract_features(url):
    return [
        len(url),
        url.count('.'),
        1 if 'https' in url else 0,
        1 if '@' in url else 0,
        1 if '-' in url else 0,
        1 if re.search(r'login|verify|bank|secure|update', url.lower()) else 0
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    confidence = None

    if request.method == 'POST':
        url = request.form['url']
        features = extract_features(url)
        prediction = model.predict([features])[0]
        prob = model.predict_proba([features])[0]
        confidence = round(max(prob) * 100, 2)

        result = "🚨 Phishing Website Detected" if prediction == 1 else "✅ Legitimate Website"

    return render_template('index.html', result=result, confidence=confidence)

if __name__ == '__main__':
    

 import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
