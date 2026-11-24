import csv
from pathlib import Path
from collections import Counter
from features import extract_features

folder = Path(__file__).parent


def analyze_dataset(filename, external=False):

    stats = {0: Counter(), 1: Counter()}

    with open(folder / filename,
              encoding="utf-8-sig", newline="") as file:

        for row in csv.DictReader(file):

            row = {
                key.strip().lower(): value
                for key, value in row.items()
            }

            url = row["url"].strip()
            label = int(row["label"])

            if external:
                label = 1 - label

            features = extract_features(url)

            stats[label]["total"] += 1
            stats[label].update(features)

    print(f"\nDATASET: {filename}")
    print("-" * 45)

    for label, values in stats.items():

        name = "Phishing" if label == 0 else "Legitimate"

        print(f"\n{name} websites:")
        print("Total:", values["total"])

        for feature, value in values.items():

            if feature != "total":
                average = value / values["total"]
                print(f"{feature}: {average:.2f}")


analyze_dataset("dataset.csv")
analyze_dataset("external_dataset.csv", external=True)