import csv
import joblib
import tldextract

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

domain_extractor = tldextract.TLDExtract(
    suffix_list_urls=()
)


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


# Collect previously seen domains

known_domains = set()

for filename in ["dataset.csv", "external_dataset.csv"]:

    print("Checking", filename)

    with open(folder / filename,
              encoding="utf-8-sig", newline="") as file:

        for row in csv.DictReader(file):

            row = {
                key.strip().lower(): value
                for key, value in row.items()
            }

            url = (row.get("url") or "").strip()

            domain = get_domain(url)

            if domain:
                known_domains.add(domain)


# Prepare final testing dataset

print("\nPreparing final testing dataset...")

records = {}
conflicts = set()

overlap = 0
duplicates = 0
invalid = 0

with open(folder / "final_dataset.csv",
          encoding="utf-8-sig", newline="") as file:

    reader = csv.DictReader(file)

    print("Dataset columns:", reader.fieldnames)

    for row in reader:

        row = {
            key.strip().lower(): value
            for key, value in row.items()
        }

        url = (row.get("url") or "").strip()

        label = (
            row.get("classlabel")
            or row.get("label")
            or ""
        ).strip()

        domain = get_domain(url)

        if not domain or label not in ("0", "1"):
            invalid += 1
            continue

        if domain in known_domains:
            overlap += 1
            continue

        if url in records:
            duplicates += 1

            if records[url] != int(label):
                conflicts.add(url)

            continue

        records[url] = int(label)


features_list = []
y = []

for url, label in records.items():

    if url in conflicts:
        continue

    features_list.append(extract_features(url))
    y.append(label)


if len(set(y)) != 2:
    raise ValueError("Both classes are required for testing.")


print("\nFINAL DATASET SUMMARY")
print("-----------------------------")

print("URLs tested:", len(y))
print("Overlapping domains excluded:", overlap)
print("Duplicates excluded:", duplicates)
print("Conflicting URLs excluded:", len(conflicts))
print("Invalid entries excluded:", invalid)
print("Label counts:", dict(Counter(y)))


# Evaluate all three versions

models = {
    "Version 1": "phishing_model.joblib",
    "Version 2": "phishing_model_v2.joblib",
    "Version 3": "phishing_model_v3.joblib"
}

results = []

for name, filename in models.items():

    print(f"\nCYBERSHIELD {name}")
    print("-----------------------------")

    saved = joblib.load(folder / filename)

    model = saved["model"]
    feature_names = saved["feature_names"]

    X = [
        [features[f] for f in feature_names]
        for features in features_list
    ]

    predictions = model.predict(X)

    result = {
        "Model": name,

        "Accuracy": accuracy_score(y, predictions),

        "Precision": precision_score(
            y, predictions,
            pos_label=0,
            zero_division=0
        ),

        "Recall": recall_score(
            y, predictions,
            pos_label=0,
            zero_division=0
        ),

        "F1-score": f1_score(
            y, predictions,
            pos_label=0,
            zero_division=0
        ),

        "Balanced accuracy": balanced_accuracy_score(
            y, predictions
        )
    }

    for metric, value in result.items():

        if metric != "Model":
            print(f"{metric}: {value:.2%}")

    tp, fn, fp, tn = confusion_matrix(
        y, predictions, labels=[0, 1]
    ).ravel()

    print("Detected phishing:", tp)
    print("Missed phishing:", fn)
    print("False alarms:", fp)
    print("Correct legitimate:", tn)

    result["Detected phishing"] = tp
    result["Missed phishing"] = fn
    result["False alarms"] = fp
    result["Correct legitimate"] = tn

    results.append(result)


# Save research results

with open(folder / "final_results.csv", "w",
          encoding="utf-8", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)


print("\nFINAL TESTING COMPLETED")
print("Results saved to final_results.csv")
