# Nuvola main class
from ..nuvola import Nuvola
# Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import *
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UsernameNotOccupied, PeerIdInvalid
import asyncio


# Add Id to commands list
Nuvola.update_commands(nuvola, "ID", {
    'name': 'id',
    'usage': [
        (".id (public chat)", "gets the id of the current chat."),
        (".id (private chat)", "gets the id of the user you are talking to."),
        (".id (reply)", "gets the id of the reply user."),
        (".id &ltusername&gt", "gets the id of the user/chat."),
    ],
    'description': 'returns a user or a chat\'s id.',
    'category': 'utilities'
})


# Id command
@Nuvola.on_message(filters.me & filters.command("id", PREFIX))
async def id_cmd(client: Nuvola, message: Message):
    # Initializing chat_to_get and chat
    chat_to_get, chat = None, None
    try:
        # Check whether an argument is provided or not
        if (len(message.command) == 2):
            # If yes, the script will get chat info based on that arg
            chat_to_get = message.command[1]
        # If not, check if the message is a reply to another message
        else:
            reply = message.reply_to_message
            # Check whether the message is a reply to another message or not
            if (reply):
                # If yes, the script will get chat info based on the user who sent the original message
                chat = reply.from_user
            else:
                # If not, the script will get chat info based on the chat id
                chat = message.chat

        # If chat_to_get is not None, get chat info based on the arg
        if (chat_to_get):
            chat = await client.get_chat(chat_to_get)

        # Edit message
        await message.edit_text(f"{chat.id}")

    # Exception: the provided arg is invalid
    except (PeerIdInvalid, UsernameNotOccupied):
        # Edit message
        await message.edit_text(ARG_INVALID)
        # Wait for x seconds
        await asyncio.sleep(2)
        # Delete message
        await message.delete()
