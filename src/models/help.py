from __future__ import annotations

from typing import TYPE_CHECKING, List, Mapping

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, Command, CommandError

if TYPE_CHECKING:
    from src.models.bot import Dandelion

class DandelionHelp(commands.DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        
    async def send_bot_help(self, mapping: Mapping[Cog, List[Command]]):
        embed = discord.Embed(
            title="Dandelion Support",
        )
        embed.description = "This is a list of commands that Dandelion supports."
        for cog, commands in mapping.items():
            if not cog or not commands:
                continue
            embed.add_field(
                name=cog.qualified_name,
                value="\n".join(f"`{command.name}` - `{command.help}`" for command in commands)
            )
        destination = self.get_destination()
        return await destination.send(embed=embed)

    async def send_cog_help(self, cog: Cog):
        embed = discord.Embed(
            title=f"{cog.qualified_name} Help",
        )
        embed.description = cog.description
        embed.add_field(
            name="Commands",
            value="\n".join(f"`{command.name}` - `{command.help}`" for command in cog.get_commands())
        )
        destination = self.get_destination()
        return await destination.send(embed=embed)

    async def send_command_help(self, command: Command):
        embed = discord.Embed(
            title=f"{command.qualified_name} Help",
        )
        embed.description = command.help or "No help found."
        destination = self.get_destination()
        return await destination.send(embed=embed)

    async def on_help_command_error(self, ctx: Context[Dandelion], error: CommandError, /) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            missing = error.retry_after
            embed = discord.Embed(title="Command on cooldown", description=f"This command is on cooldown for {missing:.01f} seconds.")
            destination = self.get_destination()
            return await destination.send(embed=embed)
        else:
            ctx.bot.logger.error(error.message)
        
        

