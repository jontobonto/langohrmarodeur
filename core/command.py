import discord
from config.config import Color, Config
from discord import app_commands
from discord.ext import commands
from utils.abc import *


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot: Langohrmarodeur = bot

    async def cog_load(self) -> None:
        context_menu = app_commands.ContextMenu(
            name="💡 Suche nach Spielern", callback=self.sng_menu
        )
        self.bot.tree.add_command(context_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command("💡 Suche nach Spielern")

    @app_commands.command(name="suche-nach-spielern")
    @app_commands.describe(
        user="Welches Mitglied soll auf die Kanäle hingewiesen werden? Standard: Niemand"
    )
    @app_commands.rename(user="mitglied")
    async def sng_command(
        self, interaction: discord.Interaction, user: discord.Member = None
    ):
        """Informationen über die Spielersuche auf dem Server."""
        # await interaction.response.defer()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Battle Royale",
                url="https://discord.com/channels/900793586898067476/1036987294718111814/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Rette die Welt",
                url="https://discord.com/channels/900793586898067476/1036987325428801576/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Kreativ",
                url="https://discord.com/channels/900793586898067476/1093575348907688136/",
            )
        )

        if user:
            return await interaction.response.send_message(
                f"🐰 Du suchst Mitspieler? Hier wirst du fündig! {user.mention}",
                view=view,
            )

        await interaction.response.send_message(
            f"🐰 Du suchst Mitspieler? Hier wirst du fündig!", view=view
        )

    # Contextmenü: 💡 Suche nach Spielern
    async def sng_menu(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        """Informationen über die Spielersuche auf dem Server."""
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Battle Royale",
                url="https://discord.com/channels/900793586898067476/1036987294718111814/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Rette die Welt",
                url="https://discord.com/channels/900793586898067476/1036987325428801576/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Kreativ",
                url="https://discord.com/channels/900793586898067476/1093575348907688136/",
            )
        )

        await interaction.response.send_message(
            f"🐰 Du suchst Mitspieler? Hier wirst du fündig! {message.author.mention}",
            view=view,
        )

    @app_commands.command()
    async def socials(self, interaction: discord.Interaction):
        """Informationen über die Sozialen Kanäle des Clans."""
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Instagram", url="https://www.instagram.com/folepu_clan/"
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Youtube",
                url="https://www.youtube.com/channel/UCFZY8wpz6h6Y_q3bH8yvjLA",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Twitter",
                url="https://twitter.com/DerHase14",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Twitch (bald verfügbar)",
                style=discord.ButtonStyle.red,
                disabled=True,
            )
        )

        await interaction.response.send_message(
            f"🐰 Hier findest du die Sozialen Kanäle des Clans.", view=view
        )


async def setup(bot: Langohrmarodeur):
    await bot.add_cog(Commands(bot))
