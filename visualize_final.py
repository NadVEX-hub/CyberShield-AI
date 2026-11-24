import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).parent

with open(folder / "final_results.csv",
          encoding="utf-8") as file:

    results = list(csv.DictReader(file))

models = [row["Model"] for row in results]

balanced = [
    float(row["Balanced accuracy"]) * 100
    for row in results
]

phishing_recall = [
    float(row["Recall"]) * 100
    for row in results
]

legitimate_recall = [
    int(row["Correct legitimate"]) /
    (int(row["Correct legitimate"]) +
     int(row["False alarms"])) * 100
    for row in results
]

x = np.arange(len(models))
width = 0.25

fig, ax = plt.subplots(figsize=(11, 7))

metrics = {
    "Balanced Accuracy": balanced,
    "Phishing Recall": phishing_recall,
    "Legitimate Recall": legitimate_recall
}

colors = ["#2563EB", "#DC2626", "#16A34A"]

for i, (name, values) in enumerate(metrics.items()):

    bars = ax.bar(
        x + (i - 1) * width,
        values,
        width,
        label=name,
        color=colors[i]
    )

    ax.bar_label(
        bars,
        fmt="%.2f%%",
        padding=3
    )

ax.set_title(
    "CyberShield AI - Model Evolution",
    fontsize=16,
    fontweight="bold"
)

ax.set_ylabel("Performance (%)")
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 110)
ax.legend()
ax.grid(axis="y", alpha=0.2)

plt.tight_layout()

plt.savefig(
    folder / "final_comparison.png",
    dpi=300
)

print("Final research graph saved successfully!")

plt.show()
