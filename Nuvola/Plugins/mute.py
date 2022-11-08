# Nuvola main class
from ..nuvola import Nuvola
# Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters
from pyrogram.types import Message
from os import path
import json

# Path to Nuvola/Utils/Json/plugins.json
path_to_file = f"{path.dirname(path.dirname(__file__))}/Utils/Json/plugins.json"

# Open the file and load the content of it in json_data
with open(path_to_file, "r") as file:
    json_data = json.load(file)

# List where the bots stores ids of muted user
muted_list = json_data["mute"]["muted"]

# Add MUTE to commands list
Nuvola.update_commands(nuvola, "MUTE", {
    'name': 'mute',
    'usage': '.mute',
    'description': 'This command will mute the user (private chat).',
    'category': 'Utilities'
})


@Nuvola.on_message(filters.me & filters.private & filters.command("mute", PREFIX))
async def mute_cmd(_, message: Message):
    # Get user
    user = message.chat
    #  If user isn't muted, mute him
    if user.id not in muted_list:
        muted_list.append(user.id)
        await message.edit_text(f"@{user.username} muted.")
        # Open the file and update the list of muted users
        with open(path_to_file, "w") as file:
            json.dump(json_data, file, indent=4)
    else:
        await message.edit_text(f"@{user.username} is already muted.")


# Add UNMUTE to commands list
Nuvola.update_commands(nuvola, "UNMUTE", {
    'name': 'unmute',
    'usage': '.unmute',
    'description': 'This command will unmute the user (private chat).',
    'category': 'Utilities'
})


@Nuvola.on_message(filters.me & filters.private & filters.command("unmute", PREFIX))
async def unmute_cmd(_, message: Message):
    # Get user
    user = message.chat
    # If the user is muted, unmute him
    if user.id in muted_list:
        muted_list.remove(user.id)
        await message.edit_text(f"@{user.username} unmuted.")
        # Open the file and update the list of muted users
        with open(path_to_file, "w") as file:
            json.dump(json_data, file, indent=4)
    else:
        await message.edit_text(f"@{user.username} isn't muted.")


# Checks if the user is muted or not
def muted(_, __, message: Message):
    return message.from_user.id in muted_list


# is_muted_filter declaration, if you don't understand what's going on here check https://docs.pyrogram.org/topics/create-filters
is_muted_filter = filters.create(muted)


# Delete all messages sent by muted users
@Nuvola.on_message(filters.incoming & is_muted_filter)
async def mute_action(_, message: Message):
    await message.delete(revoke=True)
