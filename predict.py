import joblib
from pathlib import Path
from urllib.parse import urlsplit
from features import extract_features

folder = Path(__file__).parent

saved = joblib.load(folder / "phishing_model_v3.joblib")

model = saved["model"]
feature_names = saved["feature_names"]


def predict_url(url):
    url = url.strip()

    if not url or len(url) > 4096:
        raise ValueError("Invalid URL length.")

    if any(c.isspace() for c in url):
        raise ValueError("URL must not contain spaces.")

    parsed = urlsplit(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a valid HTTP or HTTPS URL.")

    features = extract_features(url)

    data = [[features[name] for name in feature_names]]

    prediction = model.predict(data)[0]

    probabilities = model.predict_proba(data)[0]

    phishing_index = list(model.classes_).index(0)

    risk = probabilities[phishing_index] * 100

    return prediction, risk


if __name__ == "__main__":
    print("Welcome to CyberShield AI!")

    url = input("Enter a website URL: ")

    try:
        prediction, risk = predict_url(url)

        print(f"Model phishing score: {risk:.2f}%")

        if prediction == 0:
            print("Prediction: PHISHING")
            print("Avoid entering personal information.")
        else:
            print("Prediction: LIKELY LEGITIMATE")
            print("Stay cautious. Safety is not guaranteed.")

    except ValueError as error:
        print("Error:", error)
