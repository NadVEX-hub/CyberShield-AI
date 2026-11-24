import csv
import numpy as np
import joblib

from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

folder = Path(__file__).parent

saved = joblib.load(folder / "phishing_model.joblib")

model = saved["model"]
feature_names = saved["feature_names"]

X = []
y = []
groups = []

with open(folder / "processed_data.csv",
          encoding="utf-8", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:
        X.append([int(row[name]) for name in feature_names])
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

X_test = X[test_idx]
y_test = y[test_idx]

predictions = model.predict(X_test)

print("\nCYBERSHIELD AI - MODEL EVALUATION")
print("--------------------------------")

print(f"Accuracy:  {accuracy_score(y_test, predictions):.2%}")
print(f"Precision: {precision_score(y_test, predictions, pos_label=0):.2%}")
print(f"Recall:    {recall_score(y_test, predictions, pos_label=0):.2%}")
print(f"F1-score:  {f1_score(y_test, predictions, pos_label=0):.2%}")

tp, fn, fp, tn = confusion_matrix(
    y_test, predictions, labels=[0, 1]
).ravel()

print("\nConfusion Matrix")
print("Correctly detected phishing:", tp)
print("Missed phishing websites:", fn)
print("False alarms:", fp)
print("Correctly detected legitimate:", tn)
