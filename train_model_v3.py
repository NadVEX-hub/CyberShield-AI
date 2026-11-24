import csv
import numpy as np
import joblib
import tldextract

from pathlib import Path
from urllib.parse import urlsplit
from features import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix
)

folder = Path(__file__).parent

domain_extractor = tldextract.TLDExtract(
    suffix_list_urls=()
)

feature_names = [
    "url_length",
    "dot_count",
    "hyphen_count",
    "at_count",
    "digit_count",
    "question_count",
    "percent_count",
    "suspicious_words"
]

records = {}
conflicts = set()


def get_domain(url):
    try:
        parsed = urlsplit(url)

        if parsed.scheme not in ("http", "https"):
            return None

        if not parsed.hostname:
            return None

        host = parsed.hostname.lower().rstrip(".")
        host = host.encode("idna").decode("ascii")

        parts = domain_extractor(host)

        if parts.domain and parts.suffix:
            return parts.domain + "." + parts.suffix

        return host

    except (ValueError, UnicodeError):
        return None


def load_dataset(filename, external=False):

    print("Loading", filename)

    with open(folder / filename,
              encoding="utf-8-sig", newline="") as file:

        for row in csv.DictReader(file):

            row = {
                key.strip().lower(): value
                for key, value in row.items()
            }

            url = row["url"].strip()
            label = row["label"].strip()

            if label not in ("0", "1"):
                continue

            domain = get_domain(url)

            if not domain:
                continue

            label = int(label)

            if external:
                label = 1 - label

            if url in records:
                if records[url][0] != label:
                    conflicts.add(url)
                continue

            records[url] = (label, domain)


load_dataset("dataset.csv")
load_dataset("external_dataset.csv", external=True)

X = []
y = []
groups = []

print("Preparing combined dataset...")

for url, (label, domain) in records.items():

    if url in conflicts:
        continue

    features = extract_features(url)

    X.append([
        features[name]
        for name in feature_names
    ])

    y.append(label)
    groups.append(domain)

X = np.array(X)
y = np.array(y)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(X, y, groups)
)

X_train = X[train_idx]
X_test = X[test_idx]

y_train = y[train_idx]
y_test = y[test_idx]

print("Total cleaned URLs:", len(y))
print("Training samples:", len(X_train))
print("Validation samples:", len(X_test))

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("Training CyberShield Version 3...")

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nCYBERSHIELD AI VERSION 3")
print("--------------------------------")

print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")
print(f"Precision: {precision_score(y_test, predictions, pos_label=0, zero_division=0):.2%}")
print(f"Recall: {recall_score(y_test, predictions, pos_label=0, zero_division=0):.2%}")
print(f"F1-score: {f1_score(y_test, predictions, pos_label=0, zero_division=0):.2%}")
print(f"Balanced accuracy: {balanced_accuracy_score(y_test, predictions):.2%}")

tp, fn, fp, tn = confusion_matrix(
    y_test, predictions, labels=[0, 1]
).ravel()

print("\nConfusion Matrix")
print("Detected phishing:", tp)
print("Missed phishing:", fn)
print("False alarms:", fp)
print("Correct legitimate:", tn)

joblib.dump(
    {
        "model": model,
        "feature_names": feature_names
    },
    folder / "phishing_model_v3.joblib"
)

print("\nVersion 3 saved successfully!")
