import csv
import time
import numpy as np

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from features import extract_features

folder = Path(__file__).parent

feature_names = list(
    extract_features("https://example.com")
)

X = []
y = []
groups = []

print("Loading dataset...")

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

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    ),

    "Logistic Regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000)
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=15,
        random_state=42
    )
}

results = []

for name, model in models.items():

    print(f"\nTraining {name}...")

    start = time.perf_counter()

    model.fit(X_train, y_train)

    duration = time.perf_counter() - start

    predictions = model.predict(X_test)

    result = {
        "Algorithm": name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(
            y_test, predictions, pos_label=0
        ),
        "Recall": recall_score(
            y_test, predictions, pos_label=0
        ),
        "F1-score": f1_score(
            y_test, predictions, pos_label=0
        ),
        "Training time": round(duration, 2)
    }

    results.append(result)

    print(f"Accuracy: {result['Accuracy']:.2%}")
    print(f"Precision: {result['Precision']:.2%}")
    print(f"Recall: {result['Recall']:.2%}")
    print(f"F1-score: {result['F1-score']:.2%}")
    print(f"Training time: {duration:.2f} seconds")

with open(folder / "model_results.csv", "w",
          encoding="utf-8", newline="") as file:

    writer = csv.DictWriter(
        file, fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)

print("\nMODEL COMPARISON COMPLETED")

best = max(results, key=lambda r: r["F1-score"])

print("Highest test F1-score:", best["Algorithm"])
print("Results saved to model_results.csv")
