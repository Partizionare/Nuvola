# Main class
from ..nuvola import Nuvola
# Class instance
from ..__main__ import nuvola
from pyrogram import filters, enums
from pyrogram.types import Message
from ..Utils.globals import *
import asyncio
import os


# Function: dump all chat members to a file
async def dump_to_file(client: Nuvola, chat: int | str, filename: str):
    # Declaring file_path
    file_path = f"{filename}.txt"
    # Initializing dump string
    dump = ""
    # Add member infos to dump string
    async for member in client.get_chat_members(chat):
        dump += f"{member.user.id} | {member.user.username} | {member.user.first_name} | {member.user.last_name}\n"
    # Create the file and write the dump content into it
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(dump)
    # Return file_path
    return file_path


# Dump command
@Nuvola.on_message(filters.me & filters.command("dump", PREFIX))
async def dump_cmd(client: Nuvola, message: Message):
    # Check whether an argument is provided or not
    if (len(message.command) == 2):
        # If yes, the script will get chat info based on that arg
        chat_to_get = message.command[1]
    # If not, check if the message is sent in a public or private chat
    else:
        # If the message is sent in a public chat, the script will get its info
        if (message.chat.type != enums.ChatType.PRIVATE):
            chat_to_get = message.chat.id
        else:
            # The command must be used in a public chat or providing an arg
            await message.edit_text(ARG_MISSING)

    # Get chat info
    chat = await client.get_chat(chat_to_get)
    # Get all chat members and write the scraped data to a file
    file = await dump_to_file(client, chat=chat.id, filename=chat.title)
    # Id or username of the chat where you want the dump file to be sent, "me" for saved messages
    destination = "me"
    # Caption of the dump file
    caption = f"🆔 {chat.id}\n💬 {chat.invite_link}"
    # Send dump file using provided arguments
    await client.send_document(chat_id=destination, file_name=file, caption=caption)
    # Free memory
    os.remove(file)

    # Edit message
    await message.edit_text("Dump successful, check your saved messages.")
    # Wait x seconds
    await asyncio.sleep(2)
    # Delete message
    await message.delete()
