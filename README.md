# Cognevance – AI Chatbot using NLP

An intent-based chatbot: user text → NLP preprocessing → TF-IDF features → Logistic Regression intent classifier → response selection → Flask web UI.

## Workflow
1. **Data** – `src/build_dataset.py` generates `data/intents.json` (25 intents, 373 patterns, multiple responses each, plus fallback replies).
2. **Preprocessing** – `src/preprocess.py`: lowercasing, contraction expansion, punctuation removal, tokenization, stop-word removal (question words kept because they carry intent), stemming (NLTK `PorterStemmer` if installed, otherwise built-in stemmer).
3. **Features** – word 1–2-gram TF-IDF **+** character 2–4-gram TF-IDF (robust to unseen wording/typos).
4. **Model** – Logistic Regression (scikit-learn). Training data augmented with polite prefixes/suffixes.
5. **Intent recognition & response generation** – `src/chatbot.py`: predicts intent + confidence; below threshold (0.30) a fallback reply is returned; dynamic replies for time/date.
6. **UI** – Flask app (`app.py`, `templates/index.html`) with a chat page; shows predicted intent and confidence under each reply.
7. **Testing** – `tests/test_chatbot.py` (unseen sentences + leakage check + fallback check).

## Tech stack
Python 3.10+, scikit-learn, NLTK (optional), Flask, joblib, matplotlib, HTML/CSS/JS.

## Run it
```bash
pip install -r requirements.txt
python src/build_dataset.py        # create dataset
cd src && python train.py && cd .. # train, evaluate, save models/intent_model.joblib
python tests/test_chatbot.py       # manual test-suite
python src/chatbot.py              # CLI chat
python app.py                      # web UI at http://127.0.0.1:5000
```

## Results (honest numbers)
| Evaluation | Result |
|---|---|
| Hand-written unseen test sentences (20, verified not in training data) | **90 % (18/20)** – `reports/manual_test_results.txt` |
| 3-fold cross-validation on original patterns | 72.9 % |
| Random 25 % hold-out of patterns (baseline vs. augmented) | 67.0 % / 67.0 % – `reports/metrics.json` |

The hold-out and CV numbers are lower because with ~15 patterns per intent, removing a pattern removes a unique phrasing, so they are a pessimistic estimate. Augmentation did not improve hold-out accuracy; adding more real training phrases and character n-grams did (baseline 59.6 % → 67.0 % hold-out, 52.4 % → 72.9 % CV).
Known failures: *"which date is it right now"* (predicted `yes`) and *"do i need an umbrella today"* (predicted `contact_support`, low confidence 0.35) – fixable with more date/weather phrasings.
See `reports/classification_report.txt` and `reports/confusion_matrix.png` for per-intent detail.

## Project structure
```
app.py                 Flask server
src/                   build_dataset.py, preprocess.py, train.py, chatbot.py
data/intents.json      training dataset
models/                trained model (intent_model.joblib)
templates/index.html   chat UI
tests/                 test suite
reports/               metrics, classification report, confusion matrix, test log
screenshots/           demo images
```

## Improvements / future work
More data (or a public dataset), spaCy lemmatization, a TensorFlow/transformer classifier, context memory across turns, entity extraction, multilingual support.
