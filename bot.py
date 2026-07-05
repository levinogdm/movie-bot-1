import telebot
import os
import threading
from flask import Flask

# API Token & Bot Setup
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Config
PRIVATE_CHANNEL_ID = -1004307986554
MAIN_CHANNEL_ID = -1004469439263
FOOTER = "\n\n✨ Powered by Levino" # പോയിന്റ് 7: പവേർഡ് ബൈ ലെവിനോ

@app.route('/')
def home():
    return "Levino's Bot is running!"

# പോയിന്റ് 4: ജോയിൻ ചെക്ക് ഫങ്ക്ഷൻ
def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(MAIN_CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# പോയിന്റ് 1, 2, 6: പ്രൈവറ്റ് ചാനലിൽ നിന്ന് മെയിൻ ചാനലിലേക്ക് കസ്റ്റമൈസ് ചെയ്ത് പോസ്റ്റ് ചെയ്യുന്നു
@bot.channel_post_handler(chat_types=['channel'], func=lambda message: message.chat.id == PRIVATE_CHANNEL_ID)
def custom_post_to_main(message):
    bot_username = bot.get_me().username
    caption = message.caption if message.caption else "New Movie Available!"
    
    # പോയിന്റ് 3: ലിങ്കിൽ ക്ലിക്ക് ചെയ്താൽ ബോട്ടിലേക്ക് പോകുന്നു
    post_text = f"{caption}\n\nClick below to download:\nhttps://t.me/{bot_username}?start={message.message_id}{FOOTER}"
    
    # പോയിന്റ് 2: ഫോട്ടോ, വീഡിയോ, ഡോക്യുമെന്റ് എല്ലാം സപ്പോർട്ട് ചെയ്യുന്നു
    if message.photo:
        bot.send_photo(MAIN_CHANNEL_ID, message.photo[-1].file_id, caption=post_text, parse_mode='Markdown')
    elif message.video:
        bot.send_video(MAIN_CHANNEL_ID, message.video.file_id, caption=post_text, parse_mode='Markdown')
    elif message.document:
        bot.send_document(MAIN_CHANNEL_ID, message.document.file_id, caption=post_text, parse_mode='Markdown')
    else:
        bot.send_message(MAIN_CHANNEL_ID, post_text, parse_mode='Markdown')

# പോയിന്റ് 4 & 5: ബോട്ടിൽ എത്തുമ്പോൾ ജോയിൻ ചെക്ക് ചെയ്ത് ഫയൽ അയക്കുന്നു, ശേഷം ഡിലീറ്റ് ചെയ്യുന്നു
@bot.message_handler(commands=['start'])
def start(message):
    if not is_user_joined(message.from_user.id):
        bot.reply_to(message, f"Please join our main channel first to download!{FOOTER}")
        return

    args = message.text.split()
    if len(args) > 1:
        try:
            file_id = int(args[1])
            # ഫയൽ കോപ്പി ചെയ്ത് അയക്കുന്നു (ബോട്ട് ചാറ്റിൽ)
            sent_msg = bot.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=file_id)
            
            # പോയിന്റ് 5: 2 മിനിറ്റിനകം ബോട്ടിന്റെ ചാറ്റിൽ നിന്ന് മാത്രം ഡിലീറ്റ് ആകുന്നു
            threading.Timer(120, lambda: bot.delete_message(message.chat.id, sent_msg.message_id)).start()
        except Exception:
            bot.reply_to(message, f"Sorry, link expired or file not found.{FOOTER}")
    else:
        bot.reply_to(message, f"Welcome! Use the link provided in the main channel to download.{FOOTER}")

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)