"""
Test the optimized XGBoost model on the first 10 rows of Training.csv
Usage: uv run --no-sync python test_first10.py
"""
import os, joblib, pandas as pd

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
CSV_PATH   = os.path.join(BASE_DIR, "..", "Training.csv")

# ── Load artifacts ────────────────────────────────────────────────────────────
model         = joblib.load(os.path.join(MODELS_DIR, "xgboost_model.pkl"))
feature_names = joblib.load(os.path.join(MODELS_DIR, "feature_names.joblib"))
threshold     = float(joblib.load(os.path.join(MODELS_DIR, "xgb_threshold.joblib")))
raw_features  = [f for f in feature_names if not f.startswith("feat_")]

print(f"Threshold: {threshold:.4f}  |  Features: {len(feature_names)} (raw: {len(raw_features)})\n")

# ── Feature engineering (mirrors server.py) ───────────────────────────────────
def engineer_features(df):
    d = df.copy()
    def safe_sum(cols): return df[[c for c in cols if c in df.columns]].sum(axis=1)

    d["feat_social_score"]        = safe_sum(["Appears comfortable in social settings (e.g., classrooms, birthday parties)","Prefers spending time with close friend(s) over group of people with group activities","Seems emotionally or physically exhausted after socializing","Confidently initiates conversations","Appears anxious or withdrawn in unfamiliar social settings","Feels overwhelmed by the need to communicate in social situations?"])
    d["feat_communication_score"] = safe_sum(["Struggles to read facial expressions, tone, or body language","Frequently feels misunderstood during conversations","Becomes upset or frustrated when misunderstood","Struggles to express emotions with words","Rehearses or plans their conversations (phrases, always greet Good Morning/Evening, etc.) in advance","Fnds it difficult to follow multiple conversations happening at once (e.g., in a group setting)?"])
    d["feat_sensory_score"]       = safe_sum(["Sensitive to loud noises and/or bright lights or visual clutter","Avoids certain fabrics or textures due to discomfort","Affected by strong smells that others seem to tolerate","Appears overwhelmed in crowded or noisy environments"])
    d["feat_emotional_score"]     = safe_sum(["Finds it difficult to calm down after becoming upset or stressed","Finds it difficult to manage emotions during stressful interactions","Internalizes anxiety or stress without showing it","Demonstrates strong emotional reactions in intense situations (e.g., anger, crying, withdrawal)"])
    d["feat_masking_score"]       = safe_sum(["Monitors others' reactions to her actions to get a validation that she is acting appropriately","Mimics others' behavior to fit in","Avoids or struggles to maintain eye contact"])
    d["feat_routine_score"]       = safe_sum(["Demonstrates ritualized patterns of verbal or nonverbal behavior with extreme distress at small changes (Prefers routines in daily life)","Feels overwhelmed / stressed when something changes on them at the last minute or gets upset when others do not follow through on plans/promises made","Uses the same phrases or greetings in different situations"])
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

# ── Load first 10 rows ────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)
if "Field" in df.columns:
    df = df.drop(columns=["Field"])

first10    = df.head(10)
y_true     = first10["Recommendation"].astype(int).tolist()
X_raw      = first10[raw_features].astype(float)
X_eng      = engineer_features(X_raw)[feature_names]
probs      = model.predict_proba(X_eng)
preds      = (probs[:, 1] >= threshold).astype(int).tolist()

# ── Print results ─────────────────────────────────────────────────────────────
SEP = "=" * 72
print(SEP)
print(f"  {'Row':<5} {'Actual':<10} {'Predicted':<12} {'P(No ASD)':<12} {'P(ASD)':<10} {'Match'}")
print("-" * 72)

correct = 0
for i, (act, pred, prob) in enumerate(zip(y_true, preds, probs), start=1):
    match   = "✓" if act == pred else "✗"
    correct += int(act == pred)
    a_label = "ASD (1)" if act  == 1 else "No ASD (0)"
    p_label = "ASD (1)" if pred == 1 else "No ASD (0)"
    print(f"  {i:<5} {a_label:<10} {p_label:<12} {prob[0]:.4f}       {prob[1]:.4f}     {match}")

print(SEP)
print(f"  Accuracy on first 10 rows: {correct}/10  ({correct*10}%)")
print(SEP + "\n")
