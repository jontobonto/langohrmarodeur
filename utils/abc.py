import logging
import re
from textwrap import TextWrapper
from typing import Iterable, Optional, Union

import discord
from discord import (
    CategoryChannel,
    StageChannel,
    TextChannel,
    VoiceChannel,
    app_commands,
)
from discord.ext import commands

from .abc import *
from .color import Color

VocalGuildChannel = Union[VoiceChannel, StageChannel]
GuildChannel = Union[VocalGuildChannel, TextChannel, CategoryChannel]

PermissionTranslations = {
    "add_reactions": "Kanäle ansehen",
    "administrator": "Administator",
    "attach_files": "Datein anhängen",
    "ban_members": "Mitglieder bannen",
    "change_nickname": "Nickname ändern",
    "connect": "Verbinden",
    "create_instant_invite": "Sofortige Einladung erstellen",
    "create_private_threads": "Private Threads erstellen",
    "create_public_threads": "Öffentliche Threads erstellen",
    "deafen_members": "Ein- und Ausgabe von Mitgliedern deaktivieren",
    "embed_links": "Links einbetten",
    "external_emojis": "Externe Emojis verwenden",
    "kick_members": "Mitglieder kicken",
    "manage_channels": "Kanäle verwalten",
    "manage_emojis": "Emojis & Sticker verwalten",
    "manage_emojis_and_stickers": "Emojis & Sticker verwalten",
    "manage_events": "Events verwalten",
    "manage_guild": "Server verwalten",
    "manage_messages": "Nachrichten verwalten",
    "manage_nicknames": "Nicknames verwalten",
    "manage_permissions": "Berechtigungen verwalten",
    "manage_roles": "Rollen verwalten",
    "manage_threads": "Threads verwalten",
    "manage_webhooks": "WebHooks verwalten",
    "mention_everyone": "Erwähne @everyone, @here und 'Alle Rollen'",
    "moderate_members": "Mitglieder moderieren",
    "move_members": "Mitglieder verschieben",
    "mute_members": "Mitglieder stummschalten",
    "priority_speaker": "Very Important Speaker",
    "read_message_history": "Nachrichtenverlauf anzeigen",
    "read_messages": "Nachrichten lesen",
    "request_to_speak": "Redeanfrage",
    "send_messages": "Nachrichten senden",
    "send_messages_in_threads": "Nachrichten in Threads senden",
    "send_tts_messages": "Text-zu-Sprache-Nachrichten senden",
    "speak": "Sprechen",
    "stream": "Streamen",
    "use_embedded_activities": "Aktivitäten nutzen",
    "use_external_emojis": "Externe Emojis verwenden",
    "use_external_stickers": "Externe Sticker verwenden",
    "use_slash_commands": "Slash-Befehle verwenden",
    "use_voice_activation": "Sprachaktivierung verwenden",
    "view_audit_log": "Audit-Log einsehen",
    "view_channel": "Kanäle ansehen",
    "view_guild_insights": "Server-Einblicke anzeigen",
}

UnicodeCharacters = [
    "🇦",
    "🇧",
    "🇨",
    "🇩",
    "🇪",
    "🇫",
    "🇬",
    "🇭",
    "🇮",
    "🇯",
    "🇰",
    "🇱",
    "🇲",
    "🇳",
    "🇴",
    "🇵",
    "🇶",
    "🇷",
    "🇸",
    "🇹",
    "🇺",
    "🇻",
    "🇼",
    "🇽",
    "🇾",
    "🇿",
]


def chunks(iter: Iterable, size: int):
    """Yield successive sized chunks from iter."""
    for i in range(0, len(iter), size):
        yield iter[i : i + size]


def can_perform_action(author: discord.Member, member: discord.Member) -> bool | str:
    guild = author.guild if author.guild == member.guild else None

    if author == member:  # command nutzer = angegebenes mitglied
        return f"❌ Bro, was versuchst du da?"

    elif member.bot:  # angegebenes mitglied ist ein bot
        return f"❌ **{member}** ist ein Bot."

    elif member == guild.owner:  # angegebenes mitglied ist owner
        return f"❌ **{member}** ist der Besitzer des Servers."

    elif author == guild.owner:  # command nutzer ist owner
        return True  # cmd erlauben

    elif (
        author.top_role <= member.top_role
    ):  # command nutzer hat eine rolle unter der höchsten von angegeben mitglied
        return f"❌ **{member}** besitzt eine höhere oder gleichwertige Rolle."

    else:
        return True  # cmd erlauben


def shorten(
    input: str,
    *,
    _wrapper: TextWrapper = TextWrapper(
        width=100, max_lines=1, replace_whitespace=True, placeholder="…"
    ),
) -> str:
    return _wrapper.fill(" ".join(input.strip().split()))


class MessageTransformer(app_commands.Transformer):
    @staticmethod
    def _get_id_matches(interaction: discord.Interaction, argument):
        id_regex = re.compile(
            r"(?:(?P<channel_id>[0-9]{15,20})-)?(?P<message_id>[0-9]{15,20})$"
        )
        link_regex = re.compile(
            r"https?://(?:(ptb|canary|www)\.)?discord(?:app)?\.com/channels/"
            r"(?P<guild_id>[0-9]{15,20}|@me)"
            r"/(?P<channel_id>[0-9]{15,20})/(?P<message_id>[0-9]{15,20})/?$"
        )
        match = id_regex.match(argument) or link_regex.match(argument)
        if not match:
            raise commands.MessageNotFound(argument)
        data = match.groupdict()
        channel_id = (
            discord.utils._get_as_snowflake(data, "channel_id")
            or interaction.channel.id
        )
        message_id = int(data["message_id"])
        guild_id = data.get("guild_id")
        if guild_id is None:
            guild_id = interaction.guild and interaction.guild_id
        elif guild_id == "@me":
            guild_id = None
        else:
            guild_id = int(guild_id)
        return guild_id, message_id, channel_id

    @staticmethod
    def _resolve_channel(
        interaction: discord.Interaction,
        guild_id: Optional[int],
        channel_id: Optional[int],
    ) -> Optional[Union[GuildChannel, discord.Thread, discord.abc.PrivateChannel]]:
        if channel_id is None:
            # we were passed just a message id so we can assume the channel is the current context channel
            return interaction.channel

        if guild_id is not None:
            guild = interaction.client.get_guild(guild_id)
            if guild is None:
                return None
            return guild._resolve_channel(channel_id)

        return interaction.client.get_channel(channel_id)

    @classmethod
    async def transform(
        cls, interaction: discord.Interaction, value: str
    ) -> discord.Message:
        guild_id, message_id, channel_id = cls._get_id_matches(interaction, value)
        message = interaction.client._connection._get_message(message_id)
        if message:
            return message
        channel = cls._resolve_channel(interaction, guild_id, channel_id)
        if not channel or not isinstance(channel, discord.abc.Messageable):
            raise commands.ChannelNotFound(channel_id)
        try:
            return await channel.fetch_message(message_id)
        except discord.NotFound:
            raise commands.MessageNotFound(value)
        except discord.Forbidden:
            raise commands.ChannelNotReadable(channel)  # type: ignore - type-checker thinks channel could be a DMChannel at this point


class UnknownViewError(app_commands.AppCommandError):
    """Exception raised when an unknown error in a view is raised.

    This inherits from :exc:`CommandError`

    Attributes
    -----------
    original_error: :class:`Exception`
        The exception that was raised.
    item: :class:`Item`
        The item that failed the dispatch.
    interaction: :class:`~discord.Interaction`
        The interaction that led to the failure.
    view: :class:`~discord.View`:
        The view in which the error was raised.
    """

    def __init__(
        self,
        original_error: Exception,
        item: discord.ui.Item,
        interaction: discord.Interaction,
        view: discord.ui.View,
    ) -> None:
        self.original_error = original_error
        self.item = item
        self.interaction = interaction
        self.view = view

        message = f"Unknown error in view {view} for item {item}."
        super().__init__(message)


class BaseView(discord.ui.View):
    def __init__(
        self, inter: discord.Interaction, timeout: float = 180.0, **kwargs
    ) -> None:
        super().__init__(timeout=timeout)

        self.bot: Langohrmarodeur = inter.client
        self.inter: discord.Interaction = inter

        self.kwargs = kwargs

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user.id in [
            self.bot.owner_id,
            self.inter.user.id,
        ]:
            return True

        if interaction.data.get("component_type") == 2:
            embed = discord.Embed()
            embed.color = Color.red()
            embed.title = "❌ Button nutzen"
            embed.description = "Du kannst diesen Button nicht nutzen."
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif interaction.data.get("component_type") == 3:
            embed = discord.Embed()
            embed.color = Color.red()
            embed.title = "❌ Auswahlmenü nutzen"
            embed.description = "Du kannst dieses Auswahlmenü nicht nutzen."
            await interaction.response.send_message(embed=embed, ephemeral=True)

        return False

    async def on_timeout(self) -> None:
        if self.kwargs.get("disable_on_timeout", False):
            for item in self.children:
                if isinstance(item, discord.ui.Select):
                    item.options = []
                    item.max_values = 1
                    item.min_values = 1
                    item.add_option(label="Menü deaktiviert", emoji="🚫", default=True)
                item.disabled = True
                view = self
        else:
            view = None

        await self.inter.edit_original_message(view=view)

    async def on_error(
        self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction
    ) -> None:
        raise UnknownViewError(error, item, interaction, self)


class ConfirmView(BaseView):
    def __init__(
        self, inter: discord.Interaction, timeout: float = 180, **kwargs
    ) -> None:
        super().__init__(inter, timeout, **kwargs)
        self.value: bool = None
        self.interaction: discord.Interaction = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Bestätigen", style=discord.ButtonStyle.green, emoji="✔️")
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.interaction = interaction
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red, emoji="✖️")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.interaction = interaction
        self.value = False
        self.stop()

    async def on_timeout(self) -> None:
        pass


class Langohrmarodeur(commands.Bot):
    def __init__(
        self,
        command_prefix: str,
        activity: discord.BaseActivity,
        intents: discord.Intents,
    ):
        super().__init__(command_prefix, activity=activity, intents=intents)

        self._on_ready_has_run: bool = False

        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

        self.commands_guild: discord.Object = discord.Object(900793586898067476)

    async def on_ready(self):
        if self._on_ready_has_run:
            return

        self.on_ready_run = True
        self.dispatch("startup")

        self.logger.info(f"\nLogged in as {self.user}\nID: {self.user.id}")

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_extension("core.command")
        await self.load_extension("core.dev")
        await self.load_extension("core.mod")
        await self.load_extension("core.polls")
