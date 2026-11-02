"""Intent recognition + response generation."""
import json, pathlib, random, datetime
import joblib

ROOT = pathlib.Path(__file__).resolve().parent.parent
THRESHOLD = 0.30  # below this confidence -> fallback response

class Chatbot:
    def __init__(self):
        self.model = joblib.load(ROOT / "models" / "intent_model.joblib")
        data = json.loads((ROOT / "data" / "intents.json").read_text())
        self.responses = {i["tag"]: i["responses"] for i in data["intents"]}
        self.fallback = data["fallback"]

    def predict(self, text):
        probs = self.model.predict_proba([text])[0]
        idx = probs.argmax()
        return self.model.classes_[idx], float(probs[idx])

    def reply(self, text):
        if not text.strip():
            return {"intent": None, "confidence": 0.0, "response": "Please type something."}
        tag, conf = self.predict(text)
        if conf < THRESHOLD:
            return {"intent": "fallback", "confidence": conf, "response": random.choice(self.fallback)}
        resp = random.choice(self.responses[tag])
        now = datetime.datetime.now()
        resp = resp.replace("__TIME__", now.strftime("The current time is %I:%M %p.")) \
                   .replace("__DATE__", now.strftime("Today is %A, %d %B %Y."))
        return {"intent": tag, "confidence": round(conf, 3), "response": resp}

if __name__ == "__main__":
    bot = Chatbot(); print("Chatbot ready. Type quit to exit.")
    while True:
        q = input("You: ")
        if q.lower() in {"quit", "exit"}: break
        r = bot.reply(q); print(f"Bot [{r["intent"]} {r["confidence"]}]: {r["response"]}")
