from .. import tgbot
from telethon import events
import asyncio



#this will reply when user send a spesfic command
@tgbot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(''' Welcome to the RJBOT Bot!

You can use the help command:

/help - Show available commands

''')
    
#let pin the message 
@tgbot.on(events.NewMessage(incoming=True,pattern='(?i)/pin'))
async def pin_msg(event):
    chat = await event.get_chat()
    await tgbot.pin_message(chat,event.message)
    await event.respond('Message pinned!')    
    
    
@tgbot.on(events.NewMessage(incoming=True, pattern='(?i)/hey'))
async def hello(event):
    await event.reply("Hey! how are you")


#helllllp

@tgbot.on(events.NewMessage(incoming=True,pattern='(?i)/help'))
async def help(event):
    txt ='''ᵂᵉˡᶜᵒᵐᵉ ᵗᵒ ᵐʸ **RJBOT**!

Here are the available commands and their functions:

/whoami - Get information about the user.

/mypic - Download the user's profile picture.

/jokes - Get random jokes to lighten your day.

/yta <video link> - Download audio from a YouTube video.

/ytv <video link> - Download video from a YouTube video.

/tr <language code> <text> - Translate a sentence to the specified language.

/speedtest - Perform a speed test to check your downloading and uploading speed.

/txtsp <text> - Convert text to speech and generate an audio file [Support hindi text also].

/pin <text> - Pin a message to the chat. (Requires admin permission)

/wiki <query> - Make the query with wikipedia :)


Feel free to explore these commands and have fun using the bot! If you need any further assistance, feel free to ask.

Enjoy your experience with the bot!

𝖢𝗋𝖾𝖺𝗍𝖾𝖽 𝖺𝗇𝖽 𝖬𝖺𝗇𝖺𝗀𝖾𝖽 𝖡𝗒: @rahul_jerthi
'''
    await event.reply(txt)





#to download profile picture
@tgbot.on(events.NewMessage(incoming=True,pattern='(?i)/mypic'))
async def my_pic(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    photo = await tgbot.download_profile_photo(user)
    await tgbot.send_file(chat,file=photo,caption="Kesi lagi pic....!")
    
    



    
    

@tgbot.on(events.NewMessage(incoming=True,pattern='(?i)/whoami'))
async def handle_time(event):
    # Get the chat ID
    chat_id = event.chat_id

    try:
       
        
        message = event.message
        sender = await message.get_sender()
       
        await event.reply(f'''Hey its me {sender.first_name}. And i think you know me very well.\n Don't mind if you don't know me.''')
    except Exception as e:
        print(e)
    
