from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from src.models.bot import Dandelion

class Listeners(commands.Cog):
    def __init__(self, bot: Dandelion) -> None:
        self.bot = bot

    def create_command_params(self, command: commands.Command) -> str:
        return " ".join(f"<{param}>" for param in command.clean_params)


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context[Dandelion], error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            command_params = self.create_command_params(ctx.command)
            embed = discord.Embed(
                title="Missing required argument", 
                description=f"The syntax for this command is `{ctx.prefix}{ctx.command.qualified_name} {command_params}`", 
                color=0xFF0000
            )
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            return
        else:
            raise error

async def setup(bot: Dandelion) -> None:
    await bot.add_cog(Listeners(bot))