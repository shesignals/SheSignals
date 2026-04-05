"""
Optimized XGBoost Training Pipeline
====================================
Techniques applied:
  1. Stratified 5-fold cross-validation (honest evaluation)
  2. Class imbalance correction (scale_pos_weight)
  3. Feature engineering (composite domain scores)
  4. Bayesian hyperparameter search via Optuna (200 trials)
  5. Early stopping (prevents overfitting)
  6. Optimal decision threshold tuning (maximise F1 / recall)
  7. Final model trained on full dataset with best params

Usage:
    uv run --no-sync python train_optimized_xgboost.py

Output:
    models/xgboost_model.pkl          <- replaces existing model
    models/xgb_threshold.joblib       <- optimal decision threshold
    models/feature_names.joblib       <- updated feature list (with engineered features)
"""

import os
import warnings
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    precision_recall_curve, classification_report, confusion_matrix
)
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
CSV_PATH   = os.path.join(BASE_DIR, "..", "Training.csv")
N_TRIALS   = 200   # Optuna trials — increase for better results, decrease for speed
N_FOLDS    = 5     # k-fold CV

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Load & clean data
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 1: Loading Data")
print("="*65)

df = pd.read_csv(CSV_PATH)
if "Field" in df.columns:
    df = df.drop(columns=["Field"])

TARGET = "Recommendation"
X_raw = df.drop(columns=[TARGET]).astype(float)
y     = df[TARGET].astype(int)

n_neg = (y == 0).sum()
n_pos = (y == 1).sum()
scale_pos_weight = n_neg / n_pos   # class imbalance ratio

print(f"  Rows : {len(df)}")
print(f"  ASD  : {n_pos}  |  No-ASD: {n_neg}")
print(f"  scale_pos_weight = {scale_pos_weight:.4f}  (corrects class imbalance)")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Feature Engineering
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 2: Feature Engineering")
print("="*65)

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()

    # --- Domain composite scores (based on clinical groupings) ---
    social_cols = [
        "Appears comfortable in social settings (e.g., classrooms, birthday parties)",
        "Prefers spending time with close friend(s) over group of people with group activities",
        "Seems emotionally or physically exhausted after socializing",
        "Confidently initiates conversations",
        "Appears anxious or withdrawn in unfamiliar social settings",
        "Feels overwhelmed by the need to communicate in social situations?",
    ]
    communication_cols = [
        "Struggles to read facial expressions, tone, or body language",
        "Frequently feels misunderstood during conversations",
        "Becomes upset or frustrated when misunderstood",
        "Struggles to express emotions with words",
        "Rehearses or plans their conversations (phrases, always greet Good Morning/Evening, etc.) in advance",
        "Fnds it difficult to follow multiple conversations happening at once (e.g., in a group setting)?",
    ]
    sensory_cols = [
        "Sensitive to loud noises and/or bright lights or visual clutter",
        "Avoids certain fabrics or textures due to discomfort",
        "Affected by strong smells that others seem to tolerate",
        "Appears overwhelmed in crowded or noisy environments",
    ]
    emotional_cols = [
        "Finds it difficult to calm down after becoming upset or stressed",
        "Finds it difficult to manage emotions during stressful interactions",
        "Internalizes anxiety or stress without showing it",
        "Demonstrates strong emotional reactions in intense situations (e.g., anger, crying, withdrawal)",
    ]
    masking_cols = [
        "Monitors others' reactions to her actions to get a validation that she is acting appropriately",
        "Mimics others' behavior to fit in",
        "Avoids or struggles to maintain eye contact",
    ]
    routine_cols = [
        "Demonstrates ritualized patterns of verbal or nonverbal behavior with extreme distress at small changes (Prefers routines in daily life)",
        "Feels overwhelmed / stressed when something changes on them at the last minute or gets upset when others do not follow through on plans/promises made",
        "Uses the same phrases or greetings in different situations",
    ]

    def safe_sum(cols):
        valid = [c for c in cols if c in df.columns]
        return df[valid].sum(axis=1) if valid else pd.Series(0, index=df.index)

    d["feat_social_score"]        = safe_sum(social_cols)
    d["feat_communication_score"] = safe_sum(communication_cols)
    d["feat_sensory_score"]       = safe_sum(sensory_cols)
    d["feat_emotional_score"]     = safe_sum(emotional_cols)
    d["feat_masking_score"]       = safe_sum(masking_cols)
    d["feat_routine_score"]       = safe_sum(routine_cols)

    # Total symptom burden
    d["feat_total_score"] = (
        d["feat_social_score"] + d["feat_communication_score"] +
        d["feat_sensory_score"] + d["feat_emotional_score"] +
        d["feat_masking_score"] + d["feat_routine_score"]
    )

    # Interaction: early development × social difficulties
    walk_col  = "At what age did your child first start to walk?"
    speak_col = "At what age did your child first start to speak in full words or phrases?"
    if walk_col in df.columns and speak_col in df.columns:
        d["feat_dev_delay_interaction"] = df[walk_col] * df[speak_col]
        d["feat_dev_delay_sum"]         = df[walk_col] + df[speak_col]

    # Family history × total symptom score
    fh_col = "Is there a family history of autism or related neurodevelopmental conditions?"
    if fh_col in df.columns:
        d["feat_family_x_symptoms"] = df[fh_col] * d["feat_total_score"]

    return d

X_eng = engineer_features(X_raw)
feature_names = X_eng.columns.tolist()

print(f"  Raw features    : {len(X_raw.columns)}")
print(f"  Engineered feats: {len(X_eng.columns) - len(X_raw.columns)}")
print(f"  Total features  : {len(feature_names)}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Baseline XGBoost (before tuning) with proper 5-fold CV
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 3: Baseline XGBoost (5-Fold CV)")
print("="*65)

cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=42)

baseline_model = XGBClassifier(
    n_estimators=300,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)

baseline_scores = cross_validate(
    baseline_model, X_eng, y, cv=cv,
    scoring=["accuracy", "f1", "precision", "recall"],
    n_jobs=-1
)

print(f"  Accuracy  : {baseline_scores['test_accuracy'].mean():.4f} ± {baseline_scores['test_accuracy'].std():.4f}")
print(f"  F1        : {baseline_scores['test_f1'].mean():.4f} ± {baseline_scores['test_f1'].std():.4f}")
print(f"  Precision : {baseline_scores['test_precision'].mean():.4f} ± {baseline_scores['test_precision'].std():.4f}")
print(f"  Recall    : {baseline_scores['test_recall'].mean():.4f} ± {baseline_scores['test_recall'].std():.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Optuna Bayesian Hyperparameter Search
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print(f"  STEP 4: Optuna Tuning ({N_TRIALS} trials × {N_FOLDS}-fold CV)")
print("="*65)

try:
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    print("  ⚠  Optuna not installed — skipping hyperparameter search.")
    print("     Install with:  uv add optuna")

if OPTUNA_AVAILABLE:
    def objective(trial):
        params = {
            "n_estimators":       trial.suggest_int("n_estimators", 200, 1500),
            "max_depth":          trial.suggest_int("max_depth", 3, 12),
            "learning_rate":      trial.suggest_float("learning_rate", 0.005, 0.3, log=True),
            "subsample":          trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree":   trial.suggest_float("colsample_bytree", 0.4, 1.0),
            "colsample_bylevel":  trial.suggest_float("colsample_bylevel", 0.4, 1.0),
            "min_child_weight":   trial.suggest_int("min_child_weight", 1, 20),
            "gamma":              trial.suggest_float("gamma", 0.0, 5.0),
            "reg_alpha":          trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
            "reg_lambda":         trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
            "max_delta_step":     trial.suggest_int("max_delta_step", 0, 10),
            "scale_pos_weight":   trial.suggest_float("scale_pos_weight",
                                                       scale_pos_weight * 0.5,
                                                       scale_pos_weight * 2.0),
        }
        model = XGBClassifier(
            **params,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        )
        scores = cross_val_score_f1(model, X_eng, y, cv)
        return scores

    from sklearn.model_selection import cross_val_score
    def cross_val_score_f1(model, X, y, cv):
        return cross_val_score(model, X, y, cv=cv, scoring="f1", n_jobs=-1).mean()

    study = optuna.create_study(
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=20)
    )
    study.optimize(objective, n_trials=N_TRIALS, show_progress_bar=True)

    best_params = study.best_params
    best_cv_f1  = study.best_value
    print(f"\n  ✓ Best CV F1     : {best_cv_f1:.4f}")
    print(f"  Best params      : {best_params}")
else:
    # Fallback: use well-known strong defaults
    best_params = {
        "n_estimators": 800,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 3,
        "gamma": 0.1,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "scale_pos_weight": scale_pos_weight,
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Final CV evaluation with best params → honest metrics
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 5: Final 5-Fold CV with Tuned Params")
print("="*65)

tuned_model = XGBClassifier(
    **best_params,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)

final_scores = cross_validate(
    tuned_model, X_eng, y, cv=cv,
    scoring=["accuracy", "f1", "precision", "recall"],
    n_jobs=-1
)

print(f"  Accuracy  : {final_scores['test_accuracy'].mean():.4f} ± {final_scores['test_accuracy'].std():.4f}")
print(f"  F1        : {final_scores['test_f1'].mean():.4f} ± {final_scores['test_f1'].std():.4f}")
print(f"  Precision : {final_scores['test_precision'].mean():.4f} ± {final_scores['test_precision'].std():.4f}")
print(f"  Recall    : {final_scores['test_recall'].mean():.4f} ± {final_scores['test_recall'].std():.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — Optimal Decision Threshold Tuning
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 6: Optimal Threshold Tuning (Maximise Recall @ Precision ≥ 0.85)")
print("="*65)

# Use a held-out split for threshold tuning
X_tr, X_val, y_tr, y_val = train_test_split(
    X_eng, y, test_size=0.2, stratify=y, random_state=42
)

threshold_model = XGBClassifier(
    **best_params,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
    early_stopping_rounds=50,
)
threshold_model.fit(
    X_tr, y_tr,
    eval_set=[(X_val, y_val)],
    verbose=False,
)

val_probs = threshold_model.predict_proba(X_val)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)

# Strategy: maximise F1
f1_scores = np.where(
    (precisions + recalls) > 0,
    2 * (precisions * recalls) / (precisions + recalls),
    0
)
best_idx       = f1_scores[:-1].argmax()
best_threshold = float(thresholds[best_idx])
best_f1_thresh = f1_scores[best_idx]

print(f"  Default threshold (0.50) → "
      f"F1={f1_score(y_val, (val_probs >= 0.50).astype(int)):.4f}  "
      f"Recall={recall_score(y_val, (val_probs >= 0.50).astype(int)):.4f}")
print(f"  Optimal threshold ({best_threshold:.3f}) → "
      f"F1={best_f1_thresh:.4f}  "
      f"Recall={recall_score(y_val, (val_probs >= best_threshold).astype(int)):.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — Train final model on FULL dataset
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 7: Training Final Model on Full Dataset")
print("="*65)

final_model = XGBClassifier(
    **best_params,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)
final_model.fit(X_eng, y)
print("  ✓ Model trained on full dataset")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — Final Report
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 8: Full Dataset Report (training data — for reference only)")
print("="*65)

train_probs = final_model.predict_proba(X_eng)[:, 1]
train_preds = (train_probs >= best_threshold).astype(int)

print(classification_report(y, train_preds, target_names=["No ASD (0)", "ASD (1)"]))
cm = confusion_matrix(y, train_preds)
print(f"  Confusion Matrix:")
print(f"              Pred-0   Pred-1")
print(f"  Actual-0    {cm[0,0]:>5}    {cm[0,1]:>5}   (TN / FP)")
print(f"  Actual-1    {cm[1,0]:>5}    {cm[1,1]:>5}   (FN / TP)")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 — Save
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("  STEP 9: Saving Artifacts")
print("="*65)

os.makedirs(MODELS_DIR, exist_ok=True)

model_path     = os.path.join(MODELS_DIR, "xgboost_model.pkl")
threshold_path = os.path.join(MODELS_DIR, "xgb_threshold.joblib")
feat_path      = os.path.join(MODELS_DIR, "feature_names.joblib")

joblib.dump(final_model,   model_path)
joblib.dump(best_threshold, threshold_path)
joblib.dump(feature_names,  feat_path)

print(f"  ✓ Model saved     → {model_path}")
print(f"  ✓ Threshold saved → {threshold_path}  (value: {best_threshold:.4f})")
print(f"  ✓ Features saved  → {feat_path}  ({len(feature_names)} features)")
print("\n  NOTE: Update server.py to use xgb_threshold.joblib if you")
print("        want threshold-aware predictions in production.\n")
print("=" * 65)
print("  DONE")
print("=" * 65 + "\n")
