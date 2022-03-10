import discord

from .utils.bot import Langohrmarodeur

from config.config import Config

bot = Langohrmarodeur(
    command_prefix="!",
    activity=discord.Game(name="Fortnite"),
    intents=discord.Intents.all(),
)

bot.load_extension("jishaku")
bot.load_extension("commands.command")
bot.load_extension("plugins.mod")
bot.load_extension("tasks.status")

bot.run(Config.token)
