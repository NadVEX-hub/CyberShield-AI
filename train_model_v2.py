import csv
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

folder = Path(__file__).parent

# Remove the two dominant features
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

X = []
y = []
groups = []

print("Preparing CyberShield Version 2...")

with open(folder / "processed_data.csv",
          encoding="utf-8", newline="") as file:

    for row in csv.DictReader(file):
        X.append([
            int(row[name])
            for name in feature_names
        ])

        y.append(int(row["label"]))
        groups.append(row["hostname"])

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

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("Training Version 2...")

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nCYBERSHIELD AI VERSION 2")
print("----------------------------")

print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")
print(f"Precision: {precision_score(y_test, predictions, pos_label=0):.2%}")
print(f"Recall: {recall_score(y_test, predictions, pos_label=0):.2%}")
print(f"F1-score: {f1_score(y_test, predictions, pos_label=0):.2%}")

joblib.dump(
    {
        "model": model,
        "feature_names": feature_names
    },
    folder / "phishing_model_v2.joblib"
)

print("\nVersion 2 saved successfully!")
