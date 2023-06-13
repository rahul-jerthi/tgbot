from .. import tgbot
import requests
from telethon import TelegramClient, events


@tgbot.on(events.NewMessage(pattern='/joke'))
async def handle_joke(event):
    chat = await event.get_chat()

   #calling api by jio-5g
    joke_url = 'https://v2.jokeapi.dev/joke/Any'
    response = requests.get(joke_url)
    joke_data = response.json()

    if joke_data['type'] == 'single':
        joke = joke_data['joke']
    else:
        joke = f"{joke_data['setup']}\n{joke_data['delivery']}"

    
    await event.reply(joke)

