import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from keep_alive import run
from config import BOT_TOKEN, FOOTER

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📢 Updates Channel", url="https://t.me/YourChannel")
    )

    bot.send_message(
        message.chat.id,
        f"""
👋 Welcome!

This bot is online and ready.

{FOOTER}
""",
        reply_markup=keyboard
    )


@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.reply_to(
        message,
        f"""
📖 Available Commands

/start - Start Bot
/help - Help
/about - About Bot
/ping - Check Bot

{FOOTER}
"""
    )


@bot.message_handler(commands=["about"])
def about(message):
    bot.reply_to(
        message,
        f"""
🤖 Levino Bot

Version : 1.0

{FOOTER}
"""
    )


@bot.message_handler(commands=["ping"])
def ping(message):
    bot.reply_to(message, "🏓 Pong!")


def start_bot():
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    Thread(target=start_bot).start()
    run()