from pyrogram import Client, filters, types
from ..nuvola import Nuvola
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
import requests
import time
from pyrogram.errors import WebpageCurlFailed, MediaEmpty

Nuvola.update_commands(nuvola, "REDDIT", {
    'name': 'reddit',
    'usage': '.reddit &ltname channel&gt',
    'description': 'This command will send a random post from a subreddit you type.',
    'category': 'Fun'
})

@Nuvola.on_message(filters.me & filters.command("reddit", PREFIX))
async def reddit(client: Nuvola, message):
    if (len(message.command) == 2):
        try:
            reddit_channel = message.command[1]
            reddit_request = requests.get(f"https://meme-api.herokuapp.com/gimme/{reddit_channel}") 
            post = reddit_request.json()
            await message.delete()
            await client.send_photo(message.chat.id, post.get('url'), caption=f"<a href='https://reddit.com/r/{reddit_channel}'>Reddit</a> 👩‍🦽")
        except WebpageCurlFailed:
            a = await client.send_message(message.chat.id, f"⚠️ Connection error, try again.")
            time.sleep(3)
            await a.delete()
        except MediaEmpty:
            b = await client.send_message(message.chat.id, f"⚠️ Seems there is no post in this reddit...")
            time.sleep(3)
            await b.delete()
        except AttributeError:
            c = await client.send_message(message.chat.id, f"⚠️ Seems this reddit doesn't exists...")
            time.sleep(3)
            await c.delete()
