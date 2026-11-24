import csv
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from features import extract_features

folder = Path(__file__).parent

feature_names = list(extract_features("https://example.com"))

X = []
y = []
groups = []

print("Loading prepared dataset...")

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

X_train = X[train_idx]
X_test = X[test_idx]

y_train = y[train_idx]
y_test = y[test_idx]

print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))

print("Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed!")

accuracy = model.score(X_test, y_test)

print(f"Test accuracy: {accuracy:.2%}")

joblib.dump(
    {
        "model": model,
        "feature_names": feature_names
    },
    folder / "phishing_model.joblib"
)

print("AI model saved successfully!")
