import os
import telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not found!")

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Levino Bot is Running!"

@app.route("/healthz")
def health():
    return "OK", 200


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 Welcome!\n\nThis bot is online.\n\n✨ Powered by Levino"
    )


def run_bot():
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)