import discord
from discord import app_commands
from discord.ext import commands
from utils.abc import *


class PollOption:
    def __init__(self, option: str) -> None:
        self._option = option

    def __str__(self) -> str:
        return f"{self._emoji} {self._option}"

    @property
    def option(self):
        return self._option


class AddPollOption(discord.ui.Modal):
    def __init__(self) -> discord.ui.Modal:
        super().__init__(title="Option zur Umfrage hinzufügen")

        self.add_item(
            discord.ui.TextInput(
                style=discord.TextStyle.short,
                label=f"Option",
                placeholder="Welche Option soll hinzugefügt werden?",
                min_length=1,
            )
        )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.to_add = PollOption(self.children[0].value)
        self.stop()


class PollOptionsView(BaseView):
    def __init__(
        self, inter: discord.Interaction, timeout: float = 180, **kwargs
    ) -> None:
        super().__init__(inter, timeout, **kwargs)

        self.current_options: list[PollOption] = []

    def _update(self):
        self.delete_option.options = [
            discord.SelectOption(label=shorten(option.option))
            for option in self.current_options
        ]
        if not self.delete_option.options:
            self.delete_option.options = [
                discord.SelectOption(
                    label="Fill", description="Das solltest du nicht sehen!"
                )
            ]

        if len(self.current_options) >= 25:
            self.add_option.disabled = True
        else:
            self.add_option.disabled = False

        if len(self.current_options) <= 0:
            self.start_poll.disabled = True
            self.delete_option.disabled = True
        else:
            self.start_poll.disabled = False
            self.delete_option.disabled = False

    @discord.ui.select(
        placeholder="Lösche eine Option",
        disabled=True,
        options=[
            discord.SelectOption(
                label="Fill", description="Das solltest du nicht sehen!"
            )
        ],
    )
    async def delete_option(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        option = select.values[0]
        for o in self.current_options:
            if not o.option == option:
                continue
            self.current_options.remove(o)
            break

        self._update()

        embed = _create_poll_setup_embed(self.current_options)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Option hinzufügen", style=discord.ButtonStyle.blurple)
    async def add_option(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        modal = AddPollOption()
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.current_options.append(modal.to_add)
        self._update()

        embed = _create_poll_setup_embed(self.current_options)
        await self.inter.edit_original_message(embed=embed, view=self)

    @discord.ui.button(
        label="Umfrage starten", style=discord.ButtonStyle.green, disabled=True
    )
    async def start_poll(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        await interaction.response.defer()
        original_message = await interaction.original_message()
        await original_message.delete()

        embed = discord.Embed()
        embed.title = "Umfrage"
        embed.color = Color.main()
        embed.description = ""

        poll_options = enumerate(self.current_options, start=0)
        emotes_to_add = []
        for x in poll_options:
            embed.description += f"{UnicodeCharacters[x[0]]} {x[1].option}\n"
            emotes_to_add.append(UnicodeCharacters[x[0]])

        message = await interaction.channel.send(embed=embed)
        for emote in emotes_to_add:
            await message.add_reaction(emote)


def _create_poll_setup_embed(current_options: list[PollOption]) -> discord.Embed:
    embed = discord.Embed()
    embed.color = Color.green() if current_options else Color.red()
    embed.title = "Umfrage erstellen"

    if current_options:
        embed.add_field(
            name="Aktuelle Optionen",
            value="\n".join([f"• {o.option}" for o in current_options]),
        )
    else:
        embed.add_field(name="Aktuelle Optionen", value="Keine Optionen hinzugefügt")

    return embed


class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot: Langohrmarodeur = bot

    async def cog_load(self):
        pass

    async def cog_unload(self):
        pass

    @app_commands.command()
    async def poll(self, interaction: discord.Interaction):
        """Erstellt eine Umfrage und sendet sie in den Kanal."""
        view = PollOptionsView(interaction)
        embed = _create_poll_setup_embed([])
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: Langohrmarodeur):
    await bot.add_cog(Polls(bot))
