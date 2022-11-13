# Nuvola main class
from ..nuvola import Nuvola
# Nuvola istance
from ..__main__ import nuvola
from ..Utils.globals import *
from pyrogram import filters
from pyrogram.types import Message
import requests
import asyncio


# Add Reddit to commands list
Nuvola.update_commands(nuvola, "REDDIT", {
    'name': 'reddit',
    'usage': ".reddit &lt-m&gt, &lt-w&gt, &lt-c (channel_name)&gt",
    'description': 'This command will send a random post from a subreddit you type.',
    'category': 'Fun'
})


@Nuvola.on_message(filters.me & filters.command("reddit", PREFIX))
async def reddit(client: Nuvola, message: Message):
    # List of args, 'arg' : 'reddit_name'
    args = {
        '-m': 'memes',
        '-w': 'wallpaper',
    }
    # Initialize reddit variable, it contains the reddit name in which the script will search for random posts
    reddit = None
    # If not, check whether a single argument is provided or not
    if (len(message.command) == 2):
        # If yes, set variable 'reddit' value based on the arg provided
        reddit = args.get(message.command[1])
    # Check whether multiple arguments are provided or not
    elif (len(message.command) == 3):
        # If yes, check wheter the first argument is '-c' or not
        if (message.command[2] == "-c"):
            # If yes, set variable 'reddit' value based on the arg provided by the user via command
            reddit = message.command[3]

    # Check whether the reddit variable contains reddit name or not
    if (reddit):
        # If yes, try to aquire post info based on 'reddit' value
        try:
            # Edit message
            await message.edit_text(f"Getting a random post from <a href='https://reddit.com/r/{reddit}'>{reddit}</a>", disable_web_page_preview=True)
            # Fetch info using reddit api
            reddit_request = requests.get(
                f"https://meme-api.herokuapp.com/gimme/{reddit}")
            # post_info contains all post informations
            post_info = reddit_request.json()
            # Send the post fetched by the script
            await message.reply_photo(post_info.get('url'), caption=f"⛅️ Provided by Nuvola from <a href='{post_info['postLink']}'>Reddit</a>", quote=False)
            # Delete message
            await message.delete()
        # Exception: the reddit doesn't exists
        except (KeyError, AttributeError):
            error_message = await message.edit_text("⚠️ This reddit doesn't exists.")
        # Exception: general problems
        except Exception:
            error_message = await message.edit_text("⚠️ An error has occured while getting the post.")
    # If not, there is a syntax error in the command
    else:
        error_message = await message.edit_text(ARG_SYNTAX)

    # Check whether an error has occured or not
    if (error_message):
        # If yes, wait for x second(s) and delete the message
        await asyncio.sleep(2)
        await message.delete()
