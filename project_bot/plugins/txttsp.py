import asyncio
from gtts import gTTS
import os
from .. import tgbot
from telethon import TelegramClient, events



@tgbot.on(events.NewMessage(pattern='/txtsp'))
async def handle_text_to_speech(event):
    
    text = event.raw_text.replace('/txtsp ', '')

    # txt to spech ------> tts varible
    tts = gTTS(text=text, lang='hi')
    audio_file = 'output.mp3'
    tts.save(audio_file)

   

    # Send the audio file as a response
    await event.reply(file=audio_file)

    os.remove(audio_file)




