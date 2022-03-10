import discord
from config.config import Color, Config
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lm(self, 
        ctx: discord.ApplicationContext, 
        member1: discord.Member = None, 
        member2: discord.Member = None, 
        member3: discord.Member = None, 
        member4: discord.Member = None, 
        member5: discord.Member = None, 
        member6: discord.Member = None,
        member7: discord.Member = None,
        member8: discord.Member = None,
        member9: discord.Member = None,
        ):
        """Zeigt das Datum der letzten Nachricht einer oder mehrerer Personen an."""
        await ctx.defer()
        l = {member for member in (member1, member2, member3, member4, member5, member6, member7, member8, member9) if member}
        if not l:
            return await ctx.respond(f"🐰 Du musst mindestens ein Member angeben.")
        
        embed = discord.Embed()
        embed.title = "🐰 Letzte Nachricht"
        embed.color = Color.main()

        for channel in ctx.guild().text_channels:
            for message in channel.history(limit=None):
                # if message-
                pass

        await ctx.send_followup(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
