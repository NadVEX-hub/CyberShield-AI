import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).parent

with open(folder / "model_results.csv",
          encoding="utf-8") as file:
    results = list(csv.DictReader(file))

algorithms = [row["Algorithm"] for row in results]

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1-score"
]

x = np.arange(len(algorithms))
width = 0.18

colors = [
    "#2563EB",
    "#0891B2",
    "#16A34A",
    "#64748B"
]

fig, ax = plt.subplots(figsize=(12, 7))

for i, metric in enumerate(metrics):

    values = [
        float(row[metric]) * 100
        for row in results
    ]

    bars = ax.bar(
        x + (i - 1.5) * width,
        values,
        width,
        label=metric,
        color=colors[i]
    )

    ax.bar_label(
        bars,
        fmt="%.2f%%",
        fontsize=8,
        padding=3
    )

ax.set_title(
    "CyberShield AI - Model Performance Comparison",
    fontsize=16,
    fontweight="bold"
)

ax.set_ylabel("Performance (%)")
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.set_ylim(0, 110)
ax.legend(loc="lower right")
ax.grid(axis="y", alpha=0.2)

plt.tight_layout()

plt.savefig(
    folder / "model_comparison.png",
    dpi=300
)

print("Research graph saved successfully!")

plt.show()
