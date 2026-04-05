"""
Test optimized XGBoost on the first N rows of Training.csv.
Usage:
    uv run --no-sync python test_n_rows.py 100
    uv run --no-sync python test_n_rows.py 1000
"""
import os, sys, joblib, numpy as np, pandas as pd
from sklearn.metrics import (accuracy_score, f1_score,
                              precision_score, recall_score, confusion_matrix)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
CSV_PATH   = os.path.join(BASE_DIR, "..", "Training.csv")

model         = joblib.load(os.path.join(MODELS_DIR, "xgboost_model.pkl"))
feature_names = joblib.load(os.path.join(MODELS_DIR, "feature_names.joblib"))
threshold     = float(joblib.load(os.path.join(MODELS_DIR, "xgb_threshold.joblib")))
raw_features  = [f for f in feature_names if not f.startswith("feat_")]

def engineer_features(df):
    d = df.copy()
    def s(cols): return df[[c for c in cols if c in df.columns]].sum(axis=1)
    d["feat_social_score"]        = s(["Appears comfortable in social settings (e.g., classrooms, birthday parties)","Prefers spending time with close friend(s) over group of people with group activities","Seems emotionally or physically exhausted after socializing","Confidently initiates conversations","Appears anxious or withdrawn in unfamiliar social settings","Feels overwhelmed by the need to communicate in social situations?"])
    d["feat_communication_score"] = s(["Struggles to read facial expressions, tone, or body language","Frequently feels misunderstood during conversations","Becomes upset or frustrated when misunderstood","Struggles to express emotions with words","Rehearses or plans their conversations (phrases, always greet Good Morning/Evening, etc.) in advance","Fnds it difficult to follow multiple conversations happening at once (e.g., in a group setting)?"])
    d["feat_sensory_score"]       = s(["Sensitive to loud noises and/or bright lights or visual clutter","Avoids certain fabrics or textures due to discomfort","Affected by strong smells that others seem to tolerate","Appears overwhelmed in crowded or noisy environments"])
    d["feat_emotional_score"]     = s(["Finds it difficult to calm down after becoming upset or stressed","Finds it difficult to manage emotions during stressful interactions","Internalizes anxiety or stress without showing it","Demonstrates strong emotional reactions in intense situations (e.g., anger, crying, withdrawal)"])
    d["feat_masking_score"]       = s(["Monitors others' reactions to her actions to get a validation that she is acting appropriately","Mimics others' behavior to fit in","Avoids or struggles to maintain eye contact"])
    d["feat_routine_score"]       = s(["Demonstrates ritualized patterns of verbal or nonverbal behavior with extreme distress at small changes (Prefers routines in daily life)","Feels overwhelmed / stressed when something changes on them at the last minute or gets upset when others do not follow through on plans/promises made","Uses the same phrases or greetings in different situations"])
    d["feat_total_score"]         = d[["feat_social_score","feat_communication_score","feat_sensory_score","feat_emotional_score","feat_masking_score","feat_routine_score"]].sum(axis=1)
    wk = "At what age did your child first start to walk?"
    sp = "At what age did your child first start to speak in full words or phrases?"
    if wk in df.columns and sp in df.columns:
        d["feat_dev_delay_interaction"] = df[wk] * df[sp]
        d["feat_dev_delay_sum"]         = df[wk] + df[sp]
    fh = "Is there a family history of autism or related neurodevelopmental conditions?"
    if fh in df.columns:
        d["feat_family_x_symptoms"] = df[fh] * d["feat_total_score"]
    return d

df = pd.read_csv(CSV_PATH)
if "Field" in df.columns:
    df = df.drop(columns=["Field"])

subset = df.head(N)
y_true = subset["Recommendation"].astype(int).tolist()
X_raw  = subset[raw_features].astype(float)
X_eng  = engineer_features(X_raw)[feature_names]
probs  = model.predict_proba(X_eng)
preds  = (probs[:, 1] >= threshold).astype(int).tolist()

acc  = accuracy_score(y_true, preds)
f1   = f1_score(y_true, preds)
prec = precision_score(y_true, preds)
rec  = recall_score(y_true, preds)
cm   = confusion_matrix(y_true, preds)

n_asd    = sum(y_true)
n_no_asd = len(y_true) - n_asd

SEP = "=" * 65
print(f"\n{SEP}")
print(f"  XGBoost — First {N} rows  "
      f"(ASD: {n_asd}  |  No-ASD: {n_no_asd})")
print(f"  Threshold: {threshold:.4f}")
print(SEP)
print(f"  {'Metric':<12} {'Value'}")
print(f"  {'-'*30}")
print(f"  {'Accuracy':<12} {acc:.2%}")
print(f"  {'F1':<12} {f1:.2%}")
print(f"  {'Precision':<12} {prec:.2%}")
print(f"  {'Recall':<12} {rec:.2%}")
print(SEP)
print(f"\n  Confusion Matrix:")
print(f"              Pred-0   Pred-1")
print(f"  Actual-0    {cm[0,0]:>5}    {cm[0,1]:>5}   (TN / FP)")
print(f"  Actual-1    {cm[1,0]:>5}    {cm[1,1]:>5}   (FN / TP)")
print(f"\n  Correct: {sum(a==p for a,p in zip(y_true,preds))}/{N}")
print(SEP + "\n")
