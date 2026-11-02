import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from chatbot import Chatbot
bot = Chatbot()

CASES = [("good morning to you","greeting"),("see you around","goodbye"),("thank you for your help","thanks"),
 ("may i know your name","bot_identity"),("could you share a funny story","joke"),("what is the time right now","time"),
 ("can you explain natural language processing","what_is_nlp"),("how does machine learning work","what_is_ml"),
 ("where do i send my project","submission"),("do you give certificates","certificate"),
 ("i want to speak to someone from support","contact_support"),("i feel so stressed and sad","feeling_sad"),
 ("is python the best language for artificial intelligence","programming_language"),("what is the fee for this internship","pricing"),
 ("you are very smart","compliment"),("which courses do you have","courses"),
 ("which date is it right now","date"),("you are useless and dumb","insult"),("how do deep neural networks learn","what_is_deep_learning"),
 ("do i need an umbrella today","weather")]

def test_no_leakage():
    import json
    train = {p.lower() for i in json.load(open(pathlib.Path(__file__).resolve().parent.parent/'data'/'intents.json'))['intents'] for p in i['patterns']}
    leaked = [q for q,_ in CASES if q.lower() in train]
    assert not leaked, f'test sentences leaked into training data: {leaked}'

def test_intents():
    ok = 0
    for q, exp in CASES:
        got, conf = bot.predict(q); ok += got == exp
        print(f"{"PASS" if got==exp else "FAIL"}  {q!r:38} -> {got} ({conf:.2f})  expected {exp}")
    acc = ok / len(CASES); print(f"\nManual test accuracy: {ok}/{len(CASES)} = {acc:.0%}")
    assert acc >= 0.7

def test_fallback():
    r = bot.reply("xqzv blorp wug"); print("Gibberish ->", r); assert r["intent"] == "fallback"

if __name__ == "__main__":
    test_no_leakage(); test_intents(); test_fallback()
