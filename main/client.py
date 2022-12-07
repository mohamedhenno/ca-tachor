from telethon import TelegramClient

from main.config import Config

bot = TelegramClient('bot', Config.API_ID, Config.API_HASH).start(bot_token=Config.TOKEN)
