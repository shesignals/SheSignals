"""
Full dataset evaluation — runs all 3 models separately on Training.csv.
Usage:  uv run --no-sync python evaluate_models.py
"""
import os
import sys
import joblib
import numpy as np
import pandas as pd

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
CSV_PATH  = os.path.join(BASE_DIR, "..", "Training.csv")

# ── helpers ──────────────────────────────────────────────────────────────────
def confusion(y_true, y_pred):
    tp = sum(1 for a, b in zip(y_true, y_pred) if a == 1 and b == 1)
    tn = sum(1 for a, b in zip(y_true, y_pred) if a == 0 and b == 0)
    fp = sum(1 for a, b in zip(y_true, y_pred) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(y_true, y_pred) if a == 1 and b == 0)
    return tp, tn, fp, fn

def metrics(y_true, y_pred):
    tp, tn, fp, fn = confusion(y_true, y_pred)
    n   = len(y_true)
    acc = (tp + tn) / n
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1   = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    return acc, prec, rec, f1, tp, tn, fp, fn

# ── load data ────────────────────────────────────────────────────────────────
print(f"\nLoading dataset: {CSV_PATH}")
df = pd.read_csv(CSV_PATH)
print(f"  Rows: {len(df)}  |  Columns: {len(df.columns)}")

y_true = df["Recommendation"].astype(int).tolist()

# ── load feature names ───────────────────────────────────────────────────────
feat_path    = os.path.join(MODELS_DIR, "feature_names.joblib")
feature_names = joblib.load(feat_path)
print(f"  Feature names loaded: {len(feature_names)}\n")

# Build X in the exact training order
X = df[feature_names].astype(float)

# ── model registry ───────────────────────────────────────────────────────────
MODEL_FILES = {
    "Logistic Regression": os.path.join(MODELS_DIR, "logistic_regression_model.pkl"),
    "Random Forest"      : os.path.join(MODELS_DIR, "random_forest_model.pkl"),
    "XGBoost"            : os.path.join(MODELS_DIR, "xgboost_model.pkl"),
}

# ── evaluate each model ──────────────────────────────────────────────────────
results = {}

for name, path in MODEL_FILES.items():
    print(f"Loading {name} ...")
    model   = joblib.load(path)
    y_pred  = model.predict(X).astype(int).tolist()
    acc, prec, rec, f1, tp, tn, fp, fn = metrics(y_true, y_pred)
    results[name] = dict(acc=acc, prec=prec, rec=rec, f1=f1,
                         tp=tp, tn=tn, fp=fp, fn=fn, y_pred=y_pred)

# ── ensemble (majority vote) ─────────────────────────────────────────────────
preds_matrix  = [results[n]["y_pred"] for n in MODEL_FILES]
y_ens         = [1 if sum(row) >= 2 else 0 for row in zip(*preds_matrix)]
acc, prec, rec, f1, tp, tn, fp, fn = metrics(y_true, y_ens)
results["Ensemble (Majority Vote)"] = dict(acc=acc, prec=prec, rec=rec,
                                            f1=f1, tp=tp, tn=tn, fp=fp, fn=fn)

# ── print report ─────────────────────────────────────────────────────────────
SEP = "=" * 70
print(f"\n{SEP}")
print(f"  DATASET EVALUATION  —  {len(y_true)} samples  "
      f"(ASD: {sum(y_true)}  |  No-ASD: {y_true.count(0)})")
print(SEP)

header = f"{'MODEL':<28} {'ACC':>7} {'PREC':>7} {'RECALL':>8} {'F1':>7}"
print(header)
print("-" * 70)

for name, r in results.items():
    marker = "  ◄ ensemble" if "Ensemble" in name else ""
    print(f"{name:<28} {r['acc']:>7.2%} {r['prec']:>7.2%} "
          f"{r['rec']:>8.2%} {r['f1']:>7.2%}{marker}")

print(SEP)
print("\nConfusion Matrices  (rows = Actual, cols = Predicted)\n")

for name, r in results.items():
    print(f"  [{name}]")
    print(f"              Pred-0   Pred-1")
    print(f"  Actual-0    {r['tn']:>5}    {r['fp']:>5}   (TN / FP)")
    print(f"  Actual-1    {r['fn']:>5}    {r['tp']:>5}   (FN / TP)")
    print()

print(SEP)
print("Done.\n")
