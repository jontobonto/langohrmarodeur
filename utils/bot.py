import discord
from discord.ext import commands
import logging


class Langohrmarodeur(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix, intents=intents)

        self.on_ready_has_run: bool = False

        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

    async def on_ready(self):
        if self.on_ready_has_run:
            return

        self.on_ready_run = True
        self.dispatch("startup")

        print(f"\nLogged in as {self.user}\nID: {self.user.id}")
