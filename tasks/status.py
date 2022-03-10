import discord
from discord.ext import commands, tasks
import datetime


class StatusTask(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.season_1_end: datetime.datetime = datetime.datetime(
            2022, 3, 19, 8, 0, 0, tzinfo=datetime.timezone.utc
        )
        self.status.start()

    def cog_unload(self):
        self.status.cancel()

    @tasks.loop(minutes=1)
    async def status(self):
        time_until_end = self.season_1_end - datetime.datetime.now(
            datetime.timezone.utc
        )
        seconds_until_end = (
            time_until_end.days * 24 * 60 * 60
        ) + time_until_end.seconds
        mins, secs = divmod(seconds_until_end, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        months, weeks = divmod(weeks, 4)

        text = "Season 1 noch "
        if months > 0:
            text += f"{months} Mo. "
        if weeks > 0:
            text += f"{weeks} Wo. "
        if days > 0:
            text += f"{days} Ta. "
        if hours > 0:
            text += f"{hours} Std. "
        if mins > 0:
            text += f"{mins} Min. "

        await self.bot.change_presence(activity=discord.Game(text))

    @status.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(StatusTask(bot))
