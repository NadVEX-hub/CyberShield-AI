import joblib
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).parent

saved = joblib.load(folder / "phishing_model.joblib")

model = saved["model"]
feature_names = saved["feature_names"]

importance = model.feature_importances_

results = sorted(
    zip(feature_names, importance),
    key=lambda item: item[1],
    reverse=True
)

print("CYBERSHIELD AI - FEATURE IMPORTANCE")
print("-----------------------------------")

for name, value in results:
    print(f"{name}: {value:.2%}")

names = [item[0] for item in results]
values = [item[1] * 100 for item in results]

plt.figure(figsize=(10, 6))

plt.barh(names, values, color="#087CBD")

plt.gca().invert_yaxis()

plt.xlabel("Feature Importance (%)")
plt.title("CyberShield AI - Feature Importance")

plt.tight_layout()

plt.savefig(
    folder / "feature_importance.png",
    dpi=300
)

plt.show()
