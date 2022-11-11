# Nuvola main class
from ..nuvola import Nuvola
# Nuvola istance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
import re


# Add Google to commands list
Nuvola.update_commands(nuvola, "GOOGLE", {
    'name': 'google',
    'usage': '.google opt(&ltlang=locale&gt) &ltquery&gt',
    'description': 'does a google search based on the arguments provided.',
    'category': 'Utilities'
})


# Google command
@Nuvola.on_message(filters.me & filters.command("google", PREFIX))
async def google_cmd(client: Nuvola, message: Message):
    # Edit message
    await message.edit_text("Searching...")
    # Default params declaration
    lang, country = "en", "uk"
    query = '+'.join(message.command[1:])
    # Overwrite params if the arg 'lang=' is provided
    regex = re.match("^lang=[a-zA-Z]{2}.[a-zA-Z]{2}", message.command[1])
    if (regex):
        args = re.split("[\W_]", regex.group(0).lstrip("lang="))
        lang, country = args
        query = "+".join(message.command[2:])
    # Cookie to bypass google.com consent pop-up
    cookies = {'CONSENT': 'YES+cb.20221118-17-p0.en+FX+917'}
    # Params for the search
    params = {
        'q': query,
        'lr': lang,
        'hl': lang,
        'gl': country
    }
    # Get search engine page using requests
    request = requests.get(f"https://google.com/search",
                           params=params, cookies=cookies)
    # Soup
    soup = BeautifulSoup(request.content, features="html.parser")
    # Initializing text and counter
    text, counter = "⛅️ Google search\n\n", 0
    # Iter through all link in the page
    for link in soup.find_all('a'):
        # Get href attribute from 'a'element
        href = link['href']
        # Filters
        if "url?q=" in href and not "webcache" in href:
            # Get heading of links
            title = link.find_all("h3")
            # Filters
            if len(title) > 0:
                # Increase counter
                counter += 1
                # Add the formatted element scraped from the search engine
                text += f"» <a href='{href.lstrip('/url?q=').split('&sa=U')[0]}'>{title[0].getText()}</a>\n"

    # Edit message
    await message.edit_text(text, disable_web_page_preview=True)
