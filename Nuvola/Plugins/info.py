# Nuvola main class
from ..nuvola import Nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters
from pyrogram.types import Message


@Nuvola.on_message(filters.me & filters.command("info", PREFIX))
async def info(_, message: Message):
    await message.edit_text(f"**Nuvola** 0.1.0 ⛅️\n\nDeveloped **with ❤️ by:**\n\n• @Partizionare\n• @lajla\n\n**Language:** ➺ Python\n\n**Framework**: ➺ Pyrogram\n\n🔗 <a href='https://github.com/Partizionare/Nuvola'>GitHub</a>", disable_web_page_preview=True)
