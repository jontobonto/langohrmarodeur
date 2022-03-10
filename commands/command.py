import discord
from config.config import Color, Config
from discord.ext import commands
from discord import app_commands as slashcommands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slashcommands.command()
    @slashcommands.guilds(900793586898067476)
    async def sng(self, interaction: discord.Interaction, user: discord.Member = None):
        """Informationen über die Spielersuche auf dem Server."""
        # await interaction.response.defer()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Battle Royale",
                url="https://discord.com/channels/900793586898067476/920625156500635659/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Rette die Welt",
                url="https://discord.com/channels/900793586898067476/922479435792392252/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Kreativ",
                url="https://discord.com/channels/900793586898067476/920625240734838784/",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Hochstapler",
                url="https://discord.com/channels/900793586898067476/922475568388263957/",
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

    @slashcommands.command()
    @slashcommands.guilds(900793586898067476)
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

    # @slashcommands.command()
    # @slashcommands.guilds(900793586898067476)
    async def season(self, interaction: discord.Interaction):
        """Informationen zur aktuellen Season."""
        pass

def setup(bot):
    bot.add_cog(Commands(bot))
