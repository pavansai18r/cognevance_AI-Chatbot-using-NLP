import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))
from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = (request.get_json(silent=True) or {}).get("message", "")
    return jsonify(bot.reply(msg))

if __name__ == "__main__":
    app.run(debug=True)
