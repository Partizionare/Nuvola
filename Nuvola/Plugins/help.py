# Nuvola main class
from ..nuvola import Nuvola
# Nuvola istance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters
from pyrogram.types import Message


# Add HELP to commands list
Nuvola.update_commands(nuvola, "HELP", {
    'name': 'help',
    'usage': '.help',
    'description': 'This command will show you all commands available',
    'category': 'Utilities'
})


@Nuvola.on_message(filters.me & filters.command("help", PREFIX))
async def help_cmd(_, message: Message):
    # Initialize help_message string
    help_message = "⛅️ Help\n\n"
    # Just come variables to change the appearance of help_message
    n = 0
    emojis = {
        '1': '📕',
        '2': '📙',
        '3': '📘'
    }
    # Get all commands from commands list
    commands = Nuvola.get_commands(nuvola)
    for command in commands:
        n += 1 if n != 3 else -2
        # Concatenate all commands to help_message in a readable way
        help_message += f"{emojis[str(n)]} <b>{commands[command]['name']}</b>\n<b>• usage »</b> <code>{commands[command]['usage']}</code>\n<b>• category »</b> {commands[command]['category']}\n<b>• description »</b> {commands[command]['description']}\n\n"

    await message.edit_text(help_message)
