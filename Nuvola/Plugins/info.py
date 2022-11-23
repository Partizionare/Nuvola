# Import Class
from ..nuvola import Nuvola
# Import Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters, enums
from pyrogram.types import Message
import asyncio

# Add INFO to commands list
Nuvola.update_commands(nuvola, "INFO", {
    'name': 'info',
    'usage': [
        (".info", "shows infos about Nuvola")
    ],
    'description': 'returns infos about Nuvola.',
    'category': 'utilities'
})

#Some infos about Nuvola
@Nuvola.on_message(filters.me & filters.command("info", PREFIX))
async def info(client: Nuvola, message: Message):
    await message.delete()
    await client.send_message(message.chat.id, f"<a href= 'https://i.ibb.co/mzwBsBK/logo3.png'>â˜ï¸</a> <b>Nuvola 1.0.0</b> \n\nDeveloped **with â¤ï¸ by:**\nÂ» @Partizionare\nÂ» @lajla\n\nðŸ”— <a href='https://github.com/Partizionare/Nuvola'>GitHub</a>")
