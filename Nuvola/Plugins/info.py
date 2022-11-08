# Import Class
from ..nuvola import Nuvola
# Import Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters, enums
from pyrogram.types import Message
import asyncio

# some infos about the bot
@Nuvola.on_message(filters.command("info", PREFIX))
async def info(client: Nuvola, message: Message):
    await message.edit_text(f"**Nuvola** 0.1.0 ⛅️\n\nDeveloped **with ❤️ by:**\n\n• @Partizionare\n• @lajla\n\n**Language:** ➺ Python\n\n**Framework**: ➺ Pyrogram\n\n🔗 <a href='https://github.com/Partizionare/Nuvola'>GitHub</a>", disable_web_page_preview= True)
