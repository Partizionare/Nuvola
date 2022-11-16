# Import Class
from ..nuvola import Nuvola
# Import Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters
from pyrogram.types import Message
import shutil
import os
import asyncio
from datetime import datetime
import pyunpack


# Add Unzip to commands list
Nuvola.update_commands(nuvola, "UNZIP", {
    'name': 'unzip',
    'usage': [
        (".unzip (reply)", "unzips the reply file.")
    ],
    'description': 'extracts all files from the reply file.',
    'category': 'utilities'
})


# Unzip command
@Nuvola.on_message(filters.me & filters.command("unzip", PREFIX))
async def unzip_cmd(_, message: Message):
    # Reply
    reply = message.reply_to_message
    # Initizalize path variable
    path = None
    # Benchmark start
    start = datetime.now()
    try:
        # Download reply file
        path = await reply.download()
    # Exception: the user must reply to a file
    except (ValueError, AttributeError):
        await message.edit_text("⚠️ You must reply to a file.")
        await asyncio.sleep(2)

    # Allowed extensions list
    allowed_ext = [".rar", ".tar", ".tar.gz", ".tar.bz2", ".zip"]
    # Initialize ext variable, it contains the file extension
    ext = None
    # Check if the file can be extracted or not based on its extension
    for tmp in allowed_ext:
        if path.lower().endswith(tmp):
            ext = tmp
    # If ext is not None, the file can be extracted
    if (ext):
        await message.edit_text("Extracting...")
        # Extrack all files from the downloaded archive
        pyunpack.Archive(path).extractall(os.path.dirname(path))
        # Unzipped files folder
        folder = path[:len(path)-len(ext)]
        # Initialize unzipped_files, this list will contain all abs path to all extracted files
        unzipped_files = []
        # Iterate through ALL files in folder, and add the absolute path of them to unzipped_files
        for dir, _, files in os.walk(folder):
            for name in files:
                unzipped_files.append(os.path.join(dir, name))
        # Number of files sent via telegram, != len(unzipped_files) because file with size == 0 can't be sent
        counter = 0
        # Loop through all unzipped files and send them via telegram
        for file in unzipped_files:
            try:
                await message.reply_document(file, quote=False)
                counter += 1
            except ValueError:
                continue
        # Benchmark end
        end = datetime.now()
        await message.reply(f"☁️ <b>Nuvola's Unzipper</b>\n∙ Time » {(end-start).total_seconds():.2f}s\n∙ Files extracted » {counter}", quote=False)
        # Remove all extracted files
        shutil.rmtree(folder)
    # The file format is not supported
    else:
        await message.edit_text("⚠️ File format not supported.")
        await asyncio.sleep(2)

    # Remove the downloaded file
    os.remove(path)
    # Delete message
    await message.delete()
