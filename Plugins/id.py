# Import Class
from ..nuvola import Nuvola
# Import Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters, enums
from pyrogram.types import Message


# Add ID to commands list
Nuvola.update_commands(nuvola, "ID", {
    'name': 'id',
    'usage': '.id opt(&ltusername&gt)',
    'description': 'This command will get ids of users and chats.',
    'category': 'Utilities'
})


@Nuvola.on_message(filters.me & filters.command("id", PREFIX))
async def id(client: Nuvola, message: Message):
    # Check wheter an an argument is present in the command or not
    if (len(message.command) == 2):
        # If yes, get user/chat from argument
        chat_to_get = message.command[1]
        chat = await client.get_chat(chat_to_get)
        await message.edit_text(f"{chat.id}")
    # If not, check if reply
    else:
        reply = message.reply_to_message
        # Check whether the command is a reply to another message or not
        if (reply):
            # If yes, get reply user
            user = await client.get_users(reply.from_user.id)
            await message.edit_text(f"{user.id}")
        # If not, checks chat_type
        else:
            chat_type = message.chat.type
            # Check whether the command was sent in a private chat or not
            if ((chat_type == enums.ChatType.PRIVATE) | (chat_type == enums.ChatType.BOT)):
                # If yes, send the userbot id
                user = await client.get_users("me")
                await message.edit_text(f"{user.id}")
            else:
                # If not, send the chat id
                chat_id = message.chat.id
                await message.edit_text(f"{chat_id}")
