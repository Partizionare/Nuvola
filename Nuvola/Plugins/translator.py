# Nuvola main class
from ..nuvola import Nuvola
# Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX, ARG_SYNTAX
from pyrogram import filters
from pyrogram.types import Message
import asyncio
from deep_translator import GoogleTranslator
import re


# Add Translate to commands list
Nuvola.update_commands(nuvola, "TR", {
    'name': 'tr',
    'usage': [
        (".tr (reply) &lt-start&gt &lt-end&gt",
         "translates the reply message from lang start to lang end."),
        (".tr &lt-start&gt &lt-end&gt &lttext&gt",
         "translates text from lang start to lang end.")
    ],
    'description': 'translates your messages.',
    'category': 'utilities'
})


# Translate command
@Nuvola.on_message(filters.me & filters.command("tr", PREFIX))
async def translate(_, message: Message):
    # Variables initialization
    lang_start, lang_end, text_to_translate = None, None, None
    reply = message.reply_to_message
    if (len(message.command) >= 3):
        # Check whether the message is a reply to another message or not
        if reply:
            # Extract args from command
            lang_start, lang_end = message.command[1].strip(
                "-"), message.command[2].strip("-")
            text_to_translate = reply.text
        else:
            # Extract args from command, using regex
            lang_args = re.findall("[-][a-zA-Z]{1,3}", message.text)
            if (len(lang_args) == 2):
                lang_start, lang_end, index = message.command[1].strip(
                    "-"), message.command[2].strip("-"), 3
                text_to_translate = " ".join(message.command[index:])

    # If text_to_translate is not None, translate the text and edit the message
    if (text_to_translate):
        # Try to translate the text using args provided
        try:
            # Translate the text using deep_translator
            translated_text = GoogleTranslator(
                source=lang_start, target=lang_end).translate(text=text_to_translate)
            await message.edit_text(f"☁️ Nuvola's Translate ({lang_start.upper()} • {lang_end.upper()})\n» {translated_text}")
        # The args (languages) are invalid
        except Exception:
            await message.edit_text("⚠️ Invalid language. /help")
    # If text_to_translate is None, there was a syntax error in the command
    else:
        await message.edit_text(ARG_SYNTAX)
        await asyncio.sleep(2)
        await message.delete()
