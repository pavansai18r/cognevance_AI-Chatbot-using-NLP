"""Train + evaluate intent classifier. Saves model, metrics and plots."""
import json, pathlib, random
import joblib, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from preprocess import preprocess, BACKEND

ROOT = pathlib.Path(__file__).resolve().parent.parent
random.seed(42); np.random.seed(42)

def augment(text):
    pre = ["", "hey ", "please ", "can you tell me ", "i want to know "]
    suf = ["", " please", " thanks", "?"]
    return random.choice(pre) + text + random.choice(suf)

def load():
    d = json.loads((ROOT / "data" / "intents.json").read_text())
    X, y = [], []
    for it in d["intents"]:
        for p in it["patterns"]:
            X.append(p); y.append(it["tag"])
    return X, y

def make_model():
    feats = FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 2), preprocessor=preprocess, tokenizer=str.split,
                                 token_pattern=None, sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), preprocessor=preprocess,
                                 sublinear_tf=True)),
    ])
    return Pipeline([("features", feats), ("clf", LogisticRegression(C=30, max_iter=3000))])

def main():
    X, y = load()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    Xtr_aug = Xtr + [augment(t) for t in Xtr for _ in range(3)]
    ytr_aug = ytr + [l for l in ytr for _ in range(3)]

    base = make_model().fit(Xtr, ytr);          b_acc = accuracy_score(yte, base.predict(Xte))
    model = make_model().fit(Xtr_aug, ytr_aug); acc = accuracy_score(yte, model.predict(Xte))
    cv = cross_val_score(make_model(), X, y, cv=StratifiedKFold(3, shuffle=True, random_state=42)).mean()

    pred = model.predict(Xte)
    rep = classification_report(yte, pred, zero_division=0)
    metrics = {"preprocess_backend": BACKEND, "n_patterns": len(X), "n_intents": len(set(y)),
               "baseline_test_accuracy": round(b_acc, 4), "improved_test_accuracy": round(acc, 4),
               "cv_accuracy_3fold_original_data": round(float(cv), 4)}
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "metrics.json").write_text(json.dumps(metrics, indent=2))
    (ROOT / "reports" / "classification_report.txt").write_text(rep)
    print(json.dumps(metrics, indent=2)); print(rep)

    labels = sorted(set(y)); cm = confusion_matrix(yte, pred, labels=labels)
    fig, ax = plt.subplots(figsize=(10, 9)); ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels))); ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=7); ax.set_yticklabels(labels, fontsize=7)
    ax.set_title("Confusion Matrix (test set)"); plt.tight_layout()
    plt.savefig(ROOT / "reports" / "confusion_matrix.png", dpi=130); plt.close()

    final = make_model().fit(X + [augment(t) for t in X for _ in range(3)], y + [l for l in y for _ in range(3)])
    (ROOT / "models").mkdir(exist_ok=True)
    joblib.dump(final, ROOT / "models" / "intent_model.joblib")
    print("Saved models/intent_model.joblib")

if __name__ == "__main__":
    main()
