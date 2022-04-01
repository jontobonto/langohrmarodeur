import asyncio
import datetime

import discord
from config.config import Color, Config
from discord import app_commands
from discord.ext import commands
from utils.abc import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    clearGroup = app_commands.Group(
        name="clear", description="Alle Commands rund um das Löschen von Nachrichten."
    )

    @clearGroup.command(name="channel")
    # @app_commands.guilds(guild_ids=900793586898067476)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(
        quantity="Wie viele Nachrichten sollen gelöscht werden? Standard: 10"
    )
    @app_commands.describe(
        channel="Wo sollen Nachrichten gelöscht werden? Standard: aktueller Kanal."
    )
    @app_commands.rename(quantity="anzahl")
    @app_commands.rename(channel="kanal")
    async def clear_channel(
        self,
        inter: discord.Interaction,
        quantity: app_commands.Range[int, 2, 1000] = 10,
        channel: discord.TextChannel = None,
    ):
        """Löscht eine bestimmte Anzahl an Nachrichten."""
        channel: discord.TextChannel | discord.interactions.InteractionChannel = (
            channel or inter.channel
        )

        await inter.response.defer(ephemeral=True)
        deleted_messages = await channel.purge(
            limit=quantity,
            reason=f"»/clear channel quantity={quantity}« von {inter.user.id}",
        )
        await inter.followup.send(
            f"✅ Es wurden **{len(deleted_messages)}** Nachrichten in {channel.mention} gelöscht."
        )

    @clearGroup.command(name="from")
    # @app_commands.guilds(guild_ids=900793586898067476)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(
        member="Von welchem Mitglied sollen Nachrichten gelöscht werden?"
    )
    @app_commands.describe(
        quantity="Wie viele Nachrichten sollen gelöscht werden? Standard: 10"
    )
    @app_commands.describe(
        channel="Wo sollen Nachrichten gelöscht werden? Standard: aktueller Kanal."
    )
    @app_commands.rename(member="mitglied")
    @app_commands.rename(quantity="anzahl")
    @app_commands.rename(channel="kanal")
    async def clear_from(
        self,
        inter: discord.Interaction,
        member: discord.Member,
        quantity: app_commands.Range[int, 2, 200] = 10,
        channel: discord.TextChannel = None,
    ):
        """Überprüft die gegebene Anzahl an Nachrichten und löscht diese, falls sie vom gegebenen Mitglied stammen."""
        channel: discord.TextChannel | discord.interactions.InteractionChannel = (
            channel or inter.channel
        )

        def is_user(message: discord.Message):
            return message.author == member

        await inter.response.defer(ephemeral=True)
        deleted_messages = await channel.purge(
            limit=quantity,
            check=is_user,
            reason=f"»/clear from member={member} quantity={quantity}« von {inter.user.id}",
        )
        await inter.followup.send(
            f"✅ Es wurden **{len(deleted_messages)}** Nachrichten von **{member}** Nachrichten in {channel.mention} gelöscht."
        )

    @clearGroup.command(name="between")
    # @app_commands.guilds(guild_ids=900793586898067476)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(
        start="Ab welcher Naricht soll gelöscht werden? Gebe eine ID oder einen Link an."
    )
    @app_commands.describe(
        end="Bis zu welcher Nachricht soll gelöscht werden? Gebe eine ID oder einen Link an."
    )
    @app_commands.rename(start="erste_nachricht")
    @app_commands.rename(end="letzte_nachricht")
    async def clear_between(
        self,
        inter: discord.Interaction,
        start: app_commands.Transform[discord.Message, MessageTransformer],
        end: app_commands.Transform[discord.Message, MessageTransformer],
    ):
        """Löscht alle Nachrichten zwischen 2 Nachrichten.
        Aus technischen Gründen ist dies auf 1000 beschränkt. Außerdem darf die erste Nachricht nicht älter als 14 Tage alt sein.
        """
        if start.created_at > end.created_at:
            start, end = end, start

        if start.channel != inter.channel or end.channel != inter.channel:
            return await inter.response.send_message(
                f"❌ Eine der beiden angegebenen Nachrichten befindet sich nicht in {inter.channel.mention}.",
                ephemeral=True,
            )

        if start.created_at < discord.utils.utcnow() - datetime.timedelta(days=14):
            return await inter.response.send_message(
                f"❌ Die erste Nachricht ist älter als 14 Tage.", ephemeral=True
            )

        await inter.response.defer(ephemeral=True)
        deleted_messages = await inter.channel.purge(
            limit=1000,
            before=end,
            after=start,
            reason=f"»/clear between start={start.jump_url} end={end.jump_url}« von {inter.user.id}",
        )
        await inter.followup.send(
            f"✅ Es wurden {len(deleted_messages)} Nachrichten zwischen [dieser]({start.jump_url}) und [dieser]({end.jump_url}) Nachricht in {inter.channel.mention} gelöscht."
        )


async def setup(bot: Langohrmarodeur):
    await bot.add_cog(Moderation(bot))
