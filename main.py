import discord

from utils.abc import *

from config.config import Config

bot = Langohrmarodeur(
    command_prefix="!",
    activity=discord.Game(name="Fortnite"),
    intents=discord.Intents.all(),
)


@bot.event
async def on_connect():
    bot.tree.copy_global_to(guild=discord.Object(900793586898067476))
    commands = await bot.tree.sync(guild=discord.Object(900793586898067476))
    print([n.name for n in commands])


bot.run(Config.token)
