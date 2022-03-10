import discord
from discord.ext import commands
import logging


class Langohrmarodeur(commands.Bot):
    def __init__(
        self,
        command_prefix: str,
        activity: discord.BaseActivity,
        intents: discord.Intents,
    ):
        super().__init__(command_prefix, activity=activity, intents=intents)

        self.on_ready_has_run: bool = False

        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

        self.commands_guild: discord.Object = discord.Object(900793586898067476)

    async def on_connect(self):
        commands = await self.tree.sync(guild=self.commands_guild)
        self.logger.info([n.name for n in commands])

    async def on_ready(self):
        if self.on_ready_has_run:
            return

        self.on_ready_run = True
        self.dispatch("startup")

        self.logger.info(f"\nLogged in as {self.user}\nID: {self.user.id}")
