"""
Standalone model test script.
Runs a hardcoded sample through all 3 models individually and as an ensemble.
Usage: uv run python test_sample.py
"""
import os
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ── 36 feature values provided by the user ──────────────────────────────────
SAMPLE_VALUES = [
    2, 0, 0, 3, 3, 1,   # features 1-6
    3, 2, 5, 1, 5, 5,   # features 7-12
    5, 1, 4, 5, 5, 5,   # features 13-18
    1, 4, 5, 4, 4, 5,   # features 19-24
    1, 4, 5, 5, 5, 3,   # features 25-30
    5, 5, 4, 5, 4, 4,   # features 31-36
]

# ── Load feature names ───────────────────────────────────────────────────────
features_path = os.path.join(MODELS_DIR, "feature_names.joblib")
feature_names = joblib.load(features_path)
print(f"✓ Loaded {len(feature_names)} feature names\n")

assert len(feature_names) == len(SAMPLE_VALUES), (
    f"Feature count mismatch: model expects {len(feature_names)} features, "
    f"but {len(SAMPLE_VALUES)} values were provided."
)

# Build DataFrame
X = pd.DataFrame([SAMPLE_VALUES], columns=feature_names)

# ── Load and test each model ─────────────────────────────────────────────────
model_files = {
    "Logistic Regression": os.path.join(MODELS_DIR, "logistic_regression_model.pkl"),
    "Random Forest":       os.path.join(MODELS_DIR, "random_forest_model.pkl"),
    "XGBoost":             os.path.join(MODELS_DIR, "xgboost_model.pkl"),
}

model_keys = ["Logistic Regression", "Random Forest", "XGBoost"]
predictions  = []
probabilities = {0: 0.0, 1: 0.0}

print("=" * 60)
print(f"{'MODEL':<25} {'PREDICTION':<15} {'P(No ASD)':<12} {'P(ASD)'}")
print("=" * 60)

for name, path in model_files.items():
    model = joblib.load(path)
    pred  = int(model.predict(X)[0])
    prob  = model.predict_proba(X)[0].tolist()

    predictions.append(pred)
    probabilities[0] += prob[0]
    probabilities[1] += prob[1]

    label = "ASD Indicated" if pred == 1 else "No ASD"
    print(f"{name:<25} {label:<15} {prob[0]:.4f}       {prob[1]:.4f}")

# ── Ensemble (majority vote) ─────────────────────────────────────────────────
print("=" * 60)
majority_vote = 1 if sum(predictions) >= 2 else 0
avg_p0 = probabilities[0] / 3
avg_p1 = probabilities[1] / 3
ensemble_label = "ASD Indicated" if majority_vote == 1 else "No ASD"

print(f"{'ENSEMBLE (Majority Vote)':<25} {ensemble_label:<15} {avg_p0:.4f}       {avg_p1:.4f}")
print("=" * 60)
print(f"\nIndividual votes : {['ASD' if p else 'No ASD' for p in predictions]}")
print(f"Final decision   : {ensemble_label}")
if majority_vote == 1:
    print("\nRecommendation   : After consulting with 3 different solid computer programs")
    print("                   (machine learning models) we are confident that this subject")
    print("                   must see a specialist (think of this as your second and third opinion).")
else:
    print("\nRecommendation   : No immediate referral indicated.")
