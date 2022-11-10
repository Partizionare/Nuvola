# Main class
from ..nuvola import Nuvola
# Class instance
from ..__main__ import nuvola
from pyrogram import filters, enums
from pyrogram.types import Message
from ..Utils.globals import PREFIX
import asyncio
import os 


async def dump_to_file(client, chat, filename):
    file_path = f"{filename}.txt"
    dump = ""
    async for member in client.get_chat_members(chat):
        dump += f"{member.user.id} | {member.user.username} | {member.user.first_name} | {member.user.last_name}\n"
        
    with open(file_path, "w") as file:
        file.write(dump)
        
    return file_path
        
        
    
@Nuvola.on_message(filters.me & filters.command("dump", PREFIX))
async def dump_cmd(client: Nuvola, message: Message):
    if(message.chat.type == enums.ChatType.PRIVATE) & (len(message.command) == 1):
        await message.edit_text("Provide an arg.")
        await asyncio.sleep(2)
        await message.delete()
    else:
        chat = None
        if(len(message.command) == 2):
            chat = await client.get_chat(message.command[1])
        elif(message.chat.type == enums.ChatType.GROUP) | (message.chat.type == enums.ChatType.SUPERGROUP):
            chat = await client.get_chat(message.chat.id)
    
        file = await dump_to_file(client, chat.id, chat.title)
        await client.send_document("me", file, caption=f"🆔 {chat.id}\n💬 {chat.invite_link}")
        os.remove(file)
        
        await message.edit_text("Dump successful, check your saved messages.")
        await asyncio.sleep(2)
        await message.delete()
        
        
        