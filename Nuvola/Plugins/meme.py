from pyrogram import Client, filters, types
from ..nuvola import Nuvola
from ..Utils.globals import PREFIX
import requests
import time




@Nuvola.on_message(filters.me & filters.command("meme", PREFIX))
async def meme(client: Nuvola, message):
    await message.edit_text("__Uploading...__ 🔄")
    # Doing request to reddit
    p = requests.get("https://meme-api.herokuapp.com/gimme/memes")
    rr = p.json()
    await message.delete()
    # Send a random meme from the subreddit "Memes", through the request above
    await client.send_photo(message.chat.id, rr.get('url'), caption="<a href='https://reddit.com/r/Memes'>Reddit</a> 👩‍🦽")
