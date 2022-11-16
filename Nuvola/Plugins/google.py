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
    'usage': [
        (".google &ltquery&gt",
         "searches on google with default country."),
        (".google opt&lt-country&gt &ltquery&gt",
         "searches on google based on the provided country.")
    ],
    'description': 'searches on google according to the provided arguments.',
    'category': 'utilities'
})


# Google command
@Nuvola.on_message(filters.me & filters.command("google", PREFIX))
async def google_cmd(_, message: Message):
    # Edit message
    await message.edit_text("Searching...")
    # Default params declaration
    country = "us"
    query = '+'.join(message.command[1:])
    # Overwrite params if the locale arg is provided
    if (len(message.command) > 2):
        arg = re.match("[-][a-zA-Z]{1,3}", message.command[1])
        if (arg):
            country = message.command[1].lstrip("-")
            query = "+".join(message.command[2:])

    # Cookie to bypass google.com consent pop-up
    cookies = {'CONSENT': 'YES+cb.20221118-17-p0.en+FX+917'}
    # Params for the search
    params = {
        'q': query,
        'gl': country
    }
    # Get search engine page using requests
    request = requests.get(f"https://google.com/search",
                           params=params, cookies=cookies)
    # Soup
    soup = BeautifulSoup(request.content, features="html.parser")
    # Initializing text, tmp counter
    text, tmp, counter = "<b>☁️ Nuvola's Google search</b>\n", "", 0
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
                tmp += f"» <a href='{href.lstrip('/url?q=').split('&sa=U')[0]}'>{title[0].getText()}</a>\n"

    if (counter == 0):
        text += "\n» No results found."
    else:
        text += f"» query: {query}\n» country: {country.lower()}\n» elements: {counter}\n\n🔎 <b>Results</b>\n{tmp}"
    # Edit message
    await message.edit_text(text, disable_web_page_preview=True)
