import csv
from collections import Counter
from pathlib import Path

file_path = Path(__file__).parent / "dataset.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    print("Dataset columns:")
    print(reader.fieldnames)

    labels = Counter(row["label"] for row in reader)

print("Total websites:", sum(labels.values()))
print("Label counts:", dict(labels))
