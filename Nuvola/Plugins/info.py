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
    'usage': [
        (".info", "shows infos about Nuvola")
    ],
    'description': 'returns infos about Nuvola.',
    'category': 'utilities'
})


# Info command
@Nuvola.on_message(filters.command("info", PREFIX))
async def info(client: Nuvola, message: Message):
    await message.delete()
    await client.send_photo(message.chat.id, "https://ibb.co/WKzJhQ3", f"☁️ <b>Nuvola {__version__}</b>\n\nDeveloped with ❤️ by:\n» @Partizionare\n» @lajla\n\n🔗 <a href='https://github.com/Partizionare/Nuvola'>GitHub</a>")
