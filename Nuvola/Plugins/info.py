# Nuvola main class
from ..nuvola import Nuvola
# Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from ..__init__ import __version__
from pyrogram import filters
from pyrogram.types import Message

# Add INFO to commands list
Nuvola.update_commands(nuvola, "INFO", {
    'name': 'info',
    'usage': '.info',
    'description': 'This command will show info about Nuvola.',
    'category': 'Utilities'
})


# Info command
@Nuvola.on_message(filters.me & filters.command("info", PREFIX))
async def info_cmd(_, message: Message):
    await message.edit_text(f"⛅️ <b>Nuvola {__version__}</b>\n\nDeveloped <b>with ❤️ by:</b>\n\n• @Partizionare\n• @lajla\n\n🔗 <a href='https://github.com/Partizionare/Nuvola'>GitHub</a>", disable_web_page_preview=True)
