# Import Class
from ..nuvola import Nuvola
# Import Nuvola instance
from ..__main__ import nuvola
from ..Utils.globals import PREFIX
from pyrogram import filters
from pyrogram.types import Message
import shutil
import os
import re
import asyncio
from datetime import datetime

# Add ID to commands list
Nuvola.update_commands(nuvola, "UNZIP", {
    'name': 'unzip',
    'usage': '.unzip',
    'description': 'This command will unzip a rar or zip file.',
    'category': 'Utilities'
})


@Nuvola.on_message(filters.me & filters.command("unzip", PREFIX))
async def unzip_cmd(_, message: Message):
    # Reply
    reply = message.reply_to_message
    # Download the compressed archive, unpack it, and send all the unpacked files
    try:
        # Benchmark start
        start = datetime.now()
        path = await reply.download()
        # Allowed extensions list
        allowed_ext = [".tar", ".tar.gz", ".tar.bz2", ".zip"]
        # Initializing ext variable, it contains the file extension
        ext = None
        # Check if the file can be extracted or not based on its extension
        for tmp in allowed_ext:
            if path.endswith(tmp):
                ext = tmp
        # If ext is not None, the file can be extracted
        if (ext):
            folder = path.rstrip(ext)
            await message.edit_text("Extracting...")
            # Extrack all files from the downloaded archive
            shutil.unpack_archive(path, os.path.dirname(path))
            unzipped_files = os.listdir(folder)
            # Loop through all unzipped files and send them via telegram
            for file in unzipped_files:
                await message.reply_document(f"{folder}/{file}", quote=False)
            # Benchmark end
            end = datetime.now()
            await message.reply(f"☁️ <b>Nuvola Unzipper</b> » {(end-start).total_seconds():.2f}s", quote=False)
            # Remove all extracted files
            shutil.rmtree(folder)
        # The file format is not supported
        else:
            await message.edit_text("⚠️ File format not supported.")
            await asyncio.sleep(2)
        # Remove the downloaded file
        os.remove(path)
    # Exception: the user must reply to a file
    except (ValueError, AttributeError):
        await message.edit_text("⚠️ You must reply to a file.")
        await asyncio.sleep(2)

    # Delete message
    await message.delete()
