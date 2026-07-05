from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 33747387
api_hash = "aab5e6fff88631f95a572c8ce9e07234"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\nSTRING SESSION:\n")
    print(client.session.save())