import emoji
from googletrans import Translator
from telethon import events
from .. import tgbot

@tgbot.on(events.NewMessage(incoming=True, pattern="/tr (.*)"))
async def _(event):
  if event.fwd_from:
    return
  if "trim" in event.raw_text:
    return
  input_str = event.text[4:6]
  await event.reply(input_str)
  
  txt = event.text[7:]
  
  vtx=await event.reply("Translating...")
  if event.reply_to_msg_id:
    previous_message = await vtx.get_reply_message()
    text = previous_message.message 
    lan = input_str or "en"
    
  elif input_str:
    text = txt 
    lan = input_str or "en"
  else:
    await vtx.edit("`.tr LanguageCode` as reply to a message")
    return
  text = emoji.demojize(text.strip())
  lan = lan.strip()
  translator = Translator()
  translated = translator.translate(text, dest=lan)
  atxt = translated.text
  # TODO: emojify the :
  # either here, or before translation
  output_str = """**Translated By **RJBOT** **\n\nSource **( {} )**\n\nTranslation **( {} )**
   {}""".format(
     translated.src, lan, atxt
  )     
  await vtx.edit(output_str)