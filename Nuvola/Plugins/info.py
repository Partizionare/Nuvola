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
@Nuvola.on_message(filters.command("info", PREFIX))
async def info(client: Nuvola, message: Message):
    await message.delete()
    await client.send_photo(message.chat.id, "https://ibb.co/C2617yS", f"**Nuvola** {__version__} ⛅️\n\nDeveloped **with ❤️ by:**\n\n• @Partizionare\n• @lajla\n\n**Language:** ➺ Python\n\n**Framework**: ➺ Pyrogram\n\n🔗 <a href='https://github.com/Partizionare/Nuvola'>GitHub</a>")
