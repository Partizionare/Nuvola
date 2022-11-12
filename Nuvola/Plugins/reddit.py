from pyrogram import filters
from ..nuvola import Nuvola
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
import requests
import time
from pyrogram.errors import WebpageCurlFailed, MediaEmpty

Nuvola.update_commands(nuvola, "REDDIT", {
    'name': 'reddit',
    'usage': ".reddit &lt-m&gt, &lt-w&gt, &lt-c (channel_name)&gt",
    'description': 'This command will send a random post from a subreddit you type.',
    'category': 'Fun'
})

@Nuvola.on_message(filters.me & filters.command("reddit", PREFIX))
async def reddit(client: Nuvola, message):
    if (len(message.command) == 2):
        if message.command[1] == "-m":
            try:
                await message.edit_text(f"__Uploading...__ 🔁")
                meme_request = requests.get("https://meme-api.herokuapp.com/gimme/memes")
                meme = meme_request.json()
                await message.delete()
                await client.send_photo(message.chat.id, meme.get('url'), caption=f"<a href='https://reddit.com/r/memes'>Reddit</a>")
            except Exception as e:
                await message.edit_text(f"{e}")
        elif message.command[1] == "-w":
            await message.edit_text("__Uploading...__ ")
            get_wallpaper = requests.get("https://meme-api.herokuapp.com/gimme/wallpaper")
            wallpaper = get_wallpaper.json()
            await message.delete()
            await client.send_photo(message.chat.id, wallpaper.get('url'), caption = f"Here your **WallPaper** 🌇")
        else:
            invalid_syntax = await message.edit_text("⚠️ Syntax error.")
            time.sleep(3)
            await invalid_syntax.delete()
    if (len(message.command) == 3):
        if message.command[1] == "-c":
            if message.command[2]:
                try:
                    await message.edit_text(f"__Uploading post from reddit.com/r/{message.command[2]}...__", disable_web_page_preview = True)
                    reddit_channel = message.command[2]
                    reddit_request = requests.get(f"https://meme-api.herokuapp.com/gimme/{reddit_channel}") 
                    post = reddit_request.json()
                    await message.delete()
                    await client.send_photo(message.chat.id, post.get('url'), caption=f"<a href='https://reddit.com/r/{reddit_channel}'>Reddit</a>")
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
            else:
                channel_invalid = await message.edit_text("⚠️ Please provide a reddit channel name.")
                time.sleep(3)
                await channel_invalid.delete()
        else:
            invalid_syntax = await message.edit_text("⚠️ Syntax error.")
            time.sleep(3)
            await invalid_syntax.delete()
