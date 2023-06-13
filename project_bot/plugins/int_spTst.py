import os
from telethon import TelegramClient, events
from .. import tgbot


@tgbot.on(events.NewMessage(pattern='/speedtest'))
async def handle_speedtest(event):
    chat = await event.get_chat()
    message = await event.reply('Running speed test...')

    
    resp = os.popen('speedtest-cli --simple').read()
    lines = resp.split('\n')

    # Get download and upload speeds
    download_speed = None
    upload_speed = None
    for line in lines:
        if 'Download' in line:
            download_speed = line.split(':')[1].strip()
        elif 'Upload' in line:
            upload_speed = line.split(':')[1].strip()

    if download_speed is not None and upload_speed is not None:
        
        response_message = f"Download speed: {download_speed}\nUpload speed: {upload_speed}"
    else:
        response_message = "Failed to retrieve speed test results."

    # Edit the original message with the results
    await message.edit(response_message)
