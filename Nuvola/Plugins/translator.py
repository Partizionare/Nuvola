# Nuvola main class
from ..nuvola import Nuvola
# Nuvola instance
from ..Utils.globals import *
from pyrogram import filters
import asyncio
from deep_translator import GoogleTranslator



@Nuvola.on_message(filters.me & filters.command("tr", PREFIX))
async def translate(client, message):
    translator = GoogleTranslator()
    reply = message.reply_to_message
    start = message.command[1]
    lang = message.command[2]
    translator = GoogleTranslator(start, lang)
    if reply:
        if (len(message.command) == 3):
            translate_text = translator.translate(reply.text, target= lang, source = start)
            await message.edit_text(f"__Translating...__")
            await asyncio.sleep(1)
            await message.edit_text(f"{translate_text}", disable_web_page_preview=True)
        else:
            await message.edit_text("Please specify a language.")
    else:
        p = " ".join(message.command[3:])
        translation = translator.translate(p, target = lang, source = start)
        await message.edit_text("__Translating...__")
        await asyncio.sleep(1)
        await message.edit_text(f"{translation}", disable_web_page_preview = True)

            