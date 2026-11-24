import csv
import joblib
from pathlib import Path
from urllib.parse import urlsplit
from collections import Counter
from features import extract_features

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix
)

folder = Path(__file__).parent

saved = joblib.load(folder / "phishing_model_v2.joblib")

model = saved["model"]
feature_names = saved["feature_names"]


def get_hostname(url):
    try:
        parsed = urlsplit(url)

        if parsed.scheme not in ("http", "https"):
            return None

        if not parsed.hostname:
            return None

        return parsed.hostname.lower().rstrip(".").removeprefix("www.")

    except ValueError:
        return None


print("Loading original dataset...")

original_hosts = set()

with open(folder / "dataset.csv",
          encoding="utf-8-sig", newline="") as file:

    for row in csv.DictReader(file):
        host = get_hostname(row["URL"].strip())

        if host:
            original_hosts.add(host)


print("Loading external dataset...")

X = []
y = []
seen = set()

overlap = 0
duplicates = 0
invalid = 0

with open(folder / "external_dataset.csv",
          encoding="utf-8-sig", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        row = {
            key.strip().lower(): value
            for key, value in row.items()
        }

        url = row["url"].strip()
        label = row["label"].strip()

        host = get_hostname(url)

        if not host or label not in ("0", "1"):
            invalid += 1
            continue

        if host in original_hosts:
            overlap += 1
            continue

        if url in seen:
            duplicates += 1
            continue

        seen.add(url)

        features = extract_features(url)

        X.append([
            features[name]
            for name in feature_names
        ])

        # Reverse external dataset labels
        y.append(1 - int(label))


if len(set(y)) != 2:
    raise ValueError(
        "Testing requires both phishing and legitimate URLs."
    )

print("\nRunning independent evaluation...")

predictions = model.predict(X)

print("\nCYBERSHIELD AI - VERSION 2 EXTERNAL TEST")
print("--------------------------------")

print("Websites tested:", len(y))
print("Overlapping hostnames excluded:", overlap)
print("Duplicates excluded:", duplicates)
print("Invalid entries excluded:", invalid)
print("Actual label counts:", dict(Counter(y)))

print(f"\nAccuracy: {accuracy_score(y, predictions):.2%}")

print(f"Precision: {precision_score(y, predictions, pos_label=0, zero_division=0):.2%}")

print(f"Recall: {recall_score(y, predictions, pos_label=0, zero_division=0):.2%}")

print(f"F1-score: {f1_score(y, predictions, pos_label=0, zero_division=0):.2%}")

print(f"Balanced accuracy: {balanced_accuracy_score(y, predictions):.2%}")

tp, fn, fp, tn = confusion_matrix(
    y, predictions, labels=[0, 1]
).ravel()

print("\nConfusion Matrix")
print("Detected phishing:", tp)
print("Missed phishing:", fn)
print("False alarms:", fp)
print("Correct legitimate:", tn)

print("\nExternal testing completed!")
