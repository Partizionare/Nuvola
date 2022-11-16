# Nuvola main class
from ..nuvola import Nuvola
# Nuvola istance
from ..__main__ import nuvola
from ..__init__ import __version__
from ..Utils.globals import *
from pyrogram import filters
from pyrogram.types import Message
import asyncio


# Add Help to commands list
Nuvola.update_commands(nuvola, "HELP", {
    'name': 'help',
    'usage': [
        (".help", "returns the full commands list."),
        (".help &ltcmd_name&gt", "returns detailed info about a specific command.")
    ],
    'description': 'gives you infos about Nuvola\'s commands',
    'category': 'utilities'
})


# Help command
@Nuvola.on_message(filters.me & filters.command("help", PREFIX))
async def help_cmd(_, message: Message):
    # Get all commands from commands list
    commands = Nuvola.get_commands(nuvola)
    try:
        # Initializing help_message variable
        help_message = f"<b>☁️ Nuvola v{__version__}</b>\n"
        if (len(message.command) == 2):
            command = commands[message.command[1].upper()]
            help_message += f"\n📚 <b>Command</b>\n» .{command['name']}\n\n💠 <b>Category</b>\n» {command['category']}\n\n🔎 <b>Usage</b>\n"
            for usage in command['usage']:
                help_message += f"» {usage[0]}\n- {usage[1]}\n"
            help_message += f"\nℹ️ <b>Description</b>\n» {command['description']}"
        else:
            # Initialize help_message string
            help_message += f"» To get detailed infos about a specific command, use .help &ltcmd_name&gt\n\n🔑 <b>Prefixes</b>\n» | "
            for prefix in PREFIX:
                help_message += f"{prefix} | "
            help_message += "\n\n📒 <b>Commands list:</b>\n"
            # Iterate through all the available commands
            for command in commands:
                # Concatenate all commands to help_message in a readable way
                help_message += f"» <code>{commands[command]['name']}</code>\n"
        await message.edit_text(help_message)

    except KeyError:
        await message.edit_text(ARG_INVALID)
        await asyncio.sleep(2)
        await message.delete()
