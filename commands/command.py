import discord
from config.config import Color, Config
from discord.commands import slash_command
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[Config.guild_id])
    async def sng(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        """Informationen über die Spielersuche auf dem Server"""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Battle Royale", url="https://discord.com/channels/900793586898067476/920625156500635659/"))
        view.add_item(discord.ui.Button(label="Rette die Welt", url="https://discord.com/channels/900793586898067476/922479435792392252/"))
        view.add_item(discord.ui.Button(label="Kreativ", url="https://discord.com/channels/900793586898067476/920625240734838784/"))
        view.add_item(discord.ui.Button(label="Hochstapler", url="https://discord.com/channels/900793586898067476/922475568388263957/"))
        
        if user:
            return await ctx.respond(f"🐰 Du sucht Mitspieler? Hier wirst du fündig! {user.mention}", view=view)

        await ctx.respond(f"🐰 Du suchst Mitspieler? Hier wirst du fündig!", view=view)

    @slash_command(guild_ids=[Config.guild_id])
    async def social(self, ctx: discord.ApplicationContext):
        """Informationen über die Sozialen Kanäle des Clans"""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Instagram", url="https://www.instagram.com/folepu_clan/"))
        view.add_item(discord.ui.Button(label="Youtube", url="https://www.youtube.com/channel/UCFZY8wpz6h6Y_q3bH8yvjLA"))
        view.add_item(discord.ui.Button(label="Twitch (bald verfügbar)", style=discord.ButtonStyle.red, disabled=True))

        await ctx.respond(f"🐰 Hier findest du die Sozialen Kanäle des Clans.", view=view)

def setup(bot):
    bot.add_cog(Commands(bot))
