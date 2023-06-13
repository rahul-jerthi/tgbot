import asyncio
import math
import os
import time
from telethon import events
from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from .. import tgbot

@tgbot.on(events.NewMessage(incoming=True, pattern="/yt ?(.*)"))
async def download_video(event):
    url = None
    t_type = None
    typee = str(event.pattern_match.group(1))
    rl = typee.split(" ")
    url = rl[1]
    type = rl[0]
  
    await event.reply(url)
    vtx = await event.reply("`Preparing to download...`")
  
    if type == "a":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "480",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif type == "v": 
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
  
    try:
        await vtx.edit("Fetching data, please wait..")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await vtx.edit(f"{str(DE)}")
        return 
  
    c_time = time.time()
      
    if song:
        await vtx.edit(
            f"`Preparing to upload song:`\
            \n**{ytdl_data['title']}**\
            \nby *{ytdl_data['uploader']}*"
        )
        await tgbot.send_file(
            event.chat_id,
            f"{ytdl_data['id']}.mp3.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data['title']),
                    performer=str(ytdl_data["uploader"]),
                )   
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, vtx, c_time, "uploading..", f"{ytdl_data['title']}.mp3"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3.mp3") 
        await vtx.delete()    
        
    elif video:
        await vtx.edit(
            f"`Preparing to upload video:`\
            \n**{ytdl_data['title']}**\
            \nby *{ytdl_data['uploader']}*"
        )
        await tgbot.send_file(
            event.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, vtx, c_time, "Uploading..", f"{ytdl_data['title']}.mp4"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp4")
        await vtx.delete()       

async def progress(current, total, event, start, type_of_ps, file_name=None):
    
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            await event.edit(
                "{}\nFile Name: `{}`\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))

def humanbytes(size): #------> progress_bar
    
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def time_formatter(milliseconds: int) -> str:
    
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]
