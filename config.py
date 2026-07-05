import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
MAIN_CHANNEL_ID = int(os.getenv("MAIN_CHANNEL_ID"))

AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "120"))
FOOTER = os.getenv("FOOTER", "✨ Powered by Levino")