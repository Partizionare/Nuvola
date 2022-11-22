from pyrogram import Client
from . import __version__
from .Utils.config import API_ID, API_HASH
import os


# Nuvola class
class Nuvola(Client):
    def __init__(self):
        # Get current dir
        dir = os.path.dirname(__file__)
        # Plugins folder
        plugins = dict(root=f"Nuvola/Plugins")
        # Pyrogram client init
        super().__init__(
            name="Nuvola",
            api_id=API_ID,
            api_hash=API_HASH,
            app_version="Nuvola",
            plugins=plugins
        )

        # Initialize commands dict
        self.commands = {}

    # start() is called with Nuvola().run() when the Pyrogram client is started.
    async def start(self):
        await super().start()
        print(f"[✅] Nuvola online | v{__version__}")

    # stop() is called with Nuvola().run() when the Pyrogram client is stopped.
    async def stop(self):
        await super().stop()
        print("[❌] Nuvola offline.")

    # Add commands to commands dict
    def update_commands(self, key, value):
        self.commands[key] = value

    # Get commands dict
    def get_commands(self) -> dict:
        return self.commands
