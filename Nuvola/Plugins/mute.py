# Import Class
from ..nuvola import Nuvola
# Import Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters, enums
from pyrogram.types import Message
import asyncio

global mutedList
# creation of a list, in where all muted users IDs will put
mutedList = []

# function to mute an user in private chat, Nuvola will instantly delete the incoming messages of the muted user
@Nuvola.on_message(filters.private & filters.me & filters.command("mute", PREFIX))
async def mute(client: Nuvola, message: Message):
	# globalizing to make things easier
	global reply
	reply = message.reply_to_message
	if reply:
		if not message.reply_to_message.from_user.id in mutedList:
			# if the id of the user you reply to is not in list, it will be added
			mutedList.append(reply.from_user.id)
			await message.edit_text(f"@{reply.from_user.username} __muted__. O_o")
		else:
			# if is already on list, it means that the user is already muted
			await message.edit_text(f"@{reply.from_user.username} is __already muted__.")
	else:
		p = await client.get_users(message.chat.id)
		mutedList.append(message.chat.id)
		await message.edit_text(f"@{p.username} muted. O_o")
	 
# function to unmute an user in private chat, Nuvola will not delete his messages anymore
@Nuvola.on_message(filters.private & filters.me & filters.command("unmute", PREFIX))
async def unmute(client: Nuvola, message: Message):
	if message.reply_to_message:
		if message.reply_to_message.from_user.id in mutedList:
			# if the ID of the user you reply to is in the list, means that is muted, then will be unmute
			mutedList.remove(reply.from_user.id)
			await message.edit_text(f"@{reply.from_user.username} __unmuted__. ≧◡≦")
		else:
			# if the ID of the user you reply to isn't in the list, means that isn't muted
			await message.edit_text(f"{reply.from_user.username} __isn't muted__.")
	else:
		mutedList.remove(message.chat.id)
		p = await client.get_users(message.chat.id)
		await message.edit_text(f"@{p.username} unmuted. ⊙_☉")

# function to detect incoming messages of the muted IDs
@Nuvola.on_message(filters.incoming)
async def mute_action(client: Nuvola, message: Message):
	if message.from_user.id in mutedList:
		# if the ID of the user who send a message is in the list, message will be instantly delete
		await message.delete(revoke= True)
	else:
		pass



