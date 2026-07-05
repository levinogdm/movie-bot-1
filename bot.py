import telebot
import os
import threading
from flask import Flask

# Token from environment variables
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Web server for Render
app = Flask(__name__)

# Channel IDs
PRIVATE_CHANNEL_ID = -1004307986554
MAIN_CHANNEL_ID = -1004469439263

# Footer
FOOTER = "\n\nPowered by Levino"

@app.route('/')
def home():
    return "Levino's Bot is running!"

@app.route('/healthz')
def healthz():
    return "OK", 200

def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(MAIN_CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Forwarding from Private to Main (Supports all types)
@bot.channel_post_handler(chat_types=['channel'], func=lambda message: message.chat.id == PRIVATE_CHANNEL_ID, content_types=['text', 'photo', 'video', 'document', 'audio'])
def forward_to_main(message):
    bot_username = bot.get_me().username
    caption = message.caption if message.caption else "New Movie Available!"
    
    post_text = f"{caption}\n\nClick the link below to download:\nhttps://t.me/{bot_username}?start={message.message_id}{FOOTER}"
    bot.send_message(MAIN_CHANNEL_ID, post_text)

# Start command and File Delivery
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if not is_user_joined(user_id):
        bot.reply_to(message, f"Please join our main channel first to access this bot!{FOOTER}")
        return

    args = message.text.split()
    if len(args) > 1:
        try:
            file_id = int(args[1])
            # Copy file from private channel
            sent_msg = bot.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=file_id)
            
            # Delete after 2 minutes (120 seconds)
            threading.Timer(120, lambda: bot.delete_message(message.chat.id, sent_msg.message_id)).start()
        except Exception:
            bot.reply_to(message, f"Sorry, the file is not available or the link has expired.{FOOTER}")
    else:
        bot.reply_to(message, f"Welcome! Use the link provided in the main channel to download movies.{FOOTER}")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Run bot in a thread
    threading.Thread(target=run_bot).start()
    # Start web server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)