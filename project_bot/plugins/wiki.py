from telethon.sync import TelegramClient, events
import wikipedia
from .. import tgbot 


search_command = '/wiki'


@tgbot.on(events.NewMessage(pattern='/wiki .+'))
async def handle_wikipedia_search(event):
    
    search_query = event.raw_text.split(maxsplit=1)[1]

    try:
    
        result = wikipedia.summary(search_query, sentences=3)
        response = f"**RJBOT** Search results for '{search_query}':\n\n{result}"
    except wikipedia.exceptions.DisambiguationError as e:

        response = f"There are multiple results for '{search_query}'. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        
        response = f"No results found for '{search_query}'."

    
    await event.respond(response)


   
  
