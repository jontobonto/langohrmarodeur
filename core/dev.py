import discord
from discord import app_commands
from discord.ext import commands

from utils.abc import *


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot: Langohrmarodeur = bot

    @commands.command()
    async def sync(self, ctx: commands.Context):
        self.bot.tree.copy_global_to(guild=self.bot.commands_guild)
        synced: list[app_commands.AppCommand] = await self.bot.tree.sync(
            guild=self.bot.commands_guild
        )

        _updated = "\n".join([f"/{c.name}" for c in synced])
        await ctx.send(f"✅ Folgende Commands sind auf dem neusten Stand:\n{_updated}")


async def setup(bot: Langohrmarodeur):
    await bot.add_cog(Dev(bot))
