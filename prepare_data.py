import csv
from pathlib import Path
from urllib.parse import urlsplit
from features import extract_features

folder = Path(__file__).parent

records = {}
conflicts = set()

print("Preparing cybersecurity dataset...")

with open(folder / "dataset.csv", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        url = row["URL"].strip()
        label = row["label"].strip()

        if not url or label not in ("0", "1"):
            continue

        if url in records and records[url] != label:
            conflicts.add(url)

        records[url] = label

columns = list(extract_features("https://example.com"))
columns += ["hostname", "label"]

count = 0

with open(folder / "processed_data.csv", "w",
          encoding="utf-8", newline="") as file:

    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()

    for url, label in records.items():
        if url in conflicts:
            continue

        try:
            parsed = urlsplit(url)
            hostname = parsed.hostname
        except ValueError:
            continue

        if not hostname or parsed.scheme not in ("http", "https"):
            continue

        features = extract_features(url)
        features["hostname"] = hostname
        features["label"] = int(label)

        writer.writerow(features)
        count += 1

print("Data preparation completed!")
print("Total processed websites:", count)
print("Saved as processed_data.csv")
