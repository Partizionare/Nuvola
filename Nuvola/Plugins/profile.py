# Main class
from ..nuvola import Nuvola
# Class instance
from ..__main__ import nuvola
from pyrogram import filters, enums
from pyrogram.types import Message
from pyrogram.errors import UsernameNotOccupied, PeerIdInvalid
from ..Utils.globals import *
import os
import asyncio


# Add Profile commands list
Nuvola.update_commands(nuvola, "PROFILE",  {
    'name': 'profile',
    'usage': [
        (".profile (public chat)", "gets all infos about the current chat."),
        (".profile (private chat)", "gets all infos about the user you are talking to."),
        (".profile (reply)", "gets all infos about the reply user."),
        (".profile &ltusername|id&gt", "gets all infos about the user/chat.")
    ],
    'description': 'returns a user or a chat\'s profile.',
    'category': 'utilities'
})


# Compose profile info string
def compose_profile(info: tuple):
    # Initialize text string
    text = ""
    # Loop through all items in infos tuple
    for element in info:
        # Concatenate element to text string only if element is not None
        text += f"{element[0]}{element[1]}\n" if element[1] else ""

    # Return text
    return text


# Profile command
@Nuvola.on_message(filters.me & filters.command("profile", PREFIX))
async def profile_cmd(client: Nuvola, message: Message):
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
                chat_to_get = reply.from_user.id
            else:
                # If not, the script will get chat info based on the chat id
                chat_to_get = message.chat.id

        # Get chat info
        chat = await client.get_chat(chat_to_get)

        '''
        Declaring chat_info (List of tuple).
        each row of this tuple corresponds to a possible row in the final message
        consider the tuple as a sort of formatted string, the second element must be a variable,
        that variable will be checked by compose_profile() function,
        if the variable is None the row won't be added to the final message.
        check compose_profile() if you don't understand
        '''
        chat_info = [
            ("", chat.bio if chat.type ==
             enums.ChatType.PRIVATE else chat.description),
            ("• ID » ", chat.id),
            ("• Username » @", chat.username),
            ("• Name » ", chat.first_name) if chat.type == enums.ChatType.PRIVATE else (
                "• Title » ", chat.title)
        ]

        # Compose the final message based on chat_info tuple
        profile_info = compose_profile(chat_info)

        # Check whether the chat has a photo or not
        if (chat.photo):
            # If yes, download the media, send the photo with profile_info, and delete the photo from your system
            path_to_photo = await client.download_media(chat.photo.big_file_id, "photo.jpg")
            await client.send_photo(message.chat.id, path_to_photo, profile_info)
            os.remove(path_to_photo)
        else:
            # If not, send the profile_info without any photo
            await message.reply(profile_info)

    # Exception: the provided arg is invalid
    except (PeerIdInvalid, UsernameNotOccupied):
        await message.edit_text(ARG_INVALID)
        await asyncio.sleep(2)

    # Delete the message
    await message.delete()
