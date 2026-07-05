import telebot
import os
import threading
from flask import Flask

# ടോക്കൺ എൻവയോൺമെന്റിൽ നിന്ന് എടുക്കുന്നു
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# വെബ് സെർവർ (റെൻഡർ പോർട്ട് ബൈൻഡിംഗിന് വേണ്ടി)
app = Flask(__name__)

# ചാനൽ ഐഡികൾ (നിങ്ങളുടെ ഐഡി ഇവിടെ മാറ്റി നൽകുക)
MAIN_CHANNEL_ID = -1004469439263 
PRIVATE_CHANNEL_ID = -1004307986554

# ഫൂട്ടർ മെസ്സേജ്
FOOTER = "\n\nPowered by Levino"

@app.route('/')
def home():
    return "Levino's Movie Bot is running!"

def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(MAIN_CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# പ്രൈവറ്റ് ചാനലിൽ പോസ്റ്റ് വരുമ്പോൾ മെയിൻ ചാനലിലേക്ക് അയക്കുന്നു
@bot.channel_post_handler(chat_types=['channel'], func=lambda message: message.chat.id == PRIVATE_CHANNEL_ID)
def forward_to_main(message):
    caption = message.caption if message.caption else "പുതിയ സിനിമ വന്നിരിക്കുന്നു!"
    # ലിങ്ക് ഉണ്ടാക്കുന്നു
    bot_username = bot.get_me().username
    post_text = f"{caption}\n\nസിനിമ ഡൗൺലോഡ് ചെയ്യാൻ താഴെ ലിങ്കിൽ ക്ലിക്ക് ചെയ്യുക:\nhttps://t.me/{bot_username}?start={message.message_id}{FOOTER}"
    bot.send_message(MAIN_CHANNEL_ID, post_text)

# സ്റ്റാർട്ട് കമാൻഡ്
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        bot.reply_to(message, f"ആദ്യം മെയിൻ ചാനലിൽ ജോയിൻ ചെയ്യൂ!{FOOTER}")
        return

    # ഫയൽ അയക്കുന്നു
    try:
        args = message.text.split()
        if len(args) > 1:
            file_id = args[1]
            sent_msg = bot.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=int(file_id))
            
            # 2 മിനിറ്റിന് ശേഷം ഡിലീറ്റ് ചെയ്യാൻ (120 സെക്കൻഡ്)
            threading.Timer(120, lambda: bot.delete_message(message.chat.id, sent_msg.message_id)).start()
        else:
            bot.reply_to(message, f"ഈ ലിങ്ക് ഉപയോഗിച്ച് സിനിമ ഡൗൺലോഡ് ചെയ്യൂ!{FOOTER}")
    except Exception as e:
        bot.reply_to(message, f"ക്ഷമിക്കണം, ഫയൽ ലഭ്യമല്ല അല്ലെങ്കിൽ ലിങ്ക് കാലഹരണപ്പെട്ടു.{FOOTER}")

# ബോട്ട് റൺ ചെയ്യുന്ന ഭാഗം
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # ബോട്ട് റൺ ചെയ്യാൻ മറ്റൊരു ത്രെഡ് തുടങ്ങുന്നു
    threading.Thread(target=run_bot).start()
    # വെബ് സെർവർ റെൻഡറിന്റെ പോർട്ടിൽ റൺ ചെയ്യുന്നു
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)