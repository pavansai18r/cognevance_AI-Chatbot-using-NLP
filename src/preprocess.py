"""NLP preprocessing: lowercase -> clean -> tokenize -> stop-word removal -> stemming.
Uses NLTK PorterStemmer if installed, otherwise a lightweight built-in suffix stemmer."""
import re

try:
    from nltk.stem import PorterStemmer
    _stem = PorterStemmer().stem
    BACKEND = "nltk"
except Exception:
    BACKEND = "builtin"
    _SUFFIXES = ("ingly","edly","ing","ness","ions","ion","ies","ied","ed","ly","es","s")
    def _stem(w):
        for s in _SUFFIXES:
            if w.endswith(s) and len(w) - len(s) >= 3:
                return w[: -len(s)] + ("y" if s in ("ies","ied") else "")
        return w

# Question words (what/how/who/...) are KEPT: they carry intent.
STOPWORDS = {"a","an","the","is","are","am","was","were","be","to","of","in","on","at","for","and",
             "or","it","its","this","that","me","my","your","you","i","do","does","can","will","please","so","there"}
_CONTRACTIONS = {"what\u0027s":"what is","who\u0027s":"who is","it\u0027s":"it is","i\u0027m":"i am","you\u0027re":"you are",
                 "that\u0027s":"that is","how\u0027s":"how is","don\u0027t":"do not","can\u0027t":"can not","won\u0027t":"will not"}

def clean(text: str) -> str:
    text = text.lower().strip()
    for k, v in _CONTRACTIONS.items():
        text = text.replace(k, v)
    return re.sub(r"[^a-z0-9\s]", " ", text)

def tokenize(text: str):
    return clean(text).split()

def preprocess(text: str) -> str:
    tokens = [t for t in tokenize(text) if t not in STOPWORDS]
    tokens = tokens or tokenize(text)   # keep original if all were stop-words ("yes", "ok")
    return " ".join(_stem(t) for t in tokens)

if __name__ == "__main__":
    for s in ["What is the weather like today?", "Tell me a JOKE, please!!", "I am feeling lonely..."]:
        print(f"{s!r:45} -> {preprocess(s)!r}")
