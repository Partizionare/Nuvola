# Nuvola main class
from ..nuvola import Nuvola
# Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import *
from pyrogram import filters
import asyncio
import openai

#openai values
openai.organization = "org-83MGhH6GwInusqS1r8aUDWZJ"
openai.api_key = 'insert here your api key'
openai.Model.list()

# Add openai to commands list
Nuvola.update_commands(nuvola, "OPENAI", {
    'name': 'openai',
    'usage': [
        (".openai &ltphrase&gt", "generates a photo from DALL-E")
    ],
    'description': 'generates a photo from DALL-E with the phrase you insert.',
    'category': 'Fun'
})

@Nuvola.on_message(filters.me & filters.command("openai", PREFIX))
async def dalle(client, message):
    #detect if the phrase is present
    if (len(message.command) >= 2):
        x = await message.edit_text("__Generating photo from DALL-E...__")

        #Stating the phrase
        phrase = " ".join(message.command[1:])

        #creatting the image
        response = openai.Image.create(prompt = f"{phrase}", n=1, size = "1024x1024")

        #url of image
        image_url = response['data'][0]['url']
        await x.delete()

        #Sending the image
        await client.send_photo(message.chat.id, image_url, caption = f"⛅️ Provided by Nuvola from <a href='https://openai.com/dall-e-2/'>DALL-E</a>\n\n❝{phrase}❞")
    
    #if there is not any phrase
    else:
        await message.edit_text(f"⚠️ Please type a phrase.")
        await asyncio.sleep(2)
        await message.delete()
