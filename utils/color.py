from typing import Type, TypeVar

import discord

CT = TypeVar('CT', bound='Color')

class Color(discord.Color):
    @classmethod
    def main(cls: Type[CT]) -> CT:
        """A factory method that returns a :class:`Colour` with a value of ``0xFF67A0``."""
        return cls(0xFF67A0)

    @classmethod
    def invisible(cls: Type[CT]) -> CT:
        """A factoty method that returns a :class:`Colour` with a value of ``0x2F3136``."""
        return cls(0x2F3136)