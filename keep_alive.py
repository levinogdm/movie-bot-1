from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Levino Bot Running!"

@app.route("/healthz")
def health():
    return "OK", 200

def run():
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 10000)))