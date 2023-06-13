from telethon import TelegramClient
import logging
import time



api_id = "20359157"
api_hash = "2d7294040c9e5a33ffcba7b327e035ad"
bot_token = "6027381635:AAH3kX41ppsGcyp_KwWaLAcXoyGK0DWJaxc"

tgbot = TelegramClient("rjbot",api_id,api_hash).start(bot_token = bot_token)