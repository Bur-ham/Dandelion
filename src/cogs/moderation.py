from __future__ import annotations

import re
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from src.models.errors import UnguildedCommandUsage

if TYPE_CHECKING:
    from src.models.bot import Dandelion


class Moderation(commands.Cog):
    def __init__(self, bot: Dandelion):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context[Dandelion]) -> bool:
        if not ctx.guild:
            raise UnguildedCommandUsage("This command can only be used in a server.")
        return True

    def check_hierarchy(
        self, 
        ctx: commands.Context[Dandelion], 
        member: discord.Member
    ) -> bool:
        if ctx.guild.owner == ctx.author:
            return False
        if member == ctx.guild.owner:
            return f"You can't {ctx.command.name} the server owner."
        elif member == ctx.author:
            return f"You can't {ctx.command.name} yourself."
        elif member.top_role.position >= ctx.author.top_role.position:
            return f"You can't {ctx.command.name} a member with a higher role than you."
        elif ctx.guild.me.top_role.position <= member.top_role.position:
            return f"You can't {ctx.command.name} a member with a higher role than the bot."
        else:
            return False

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context[Dandelion], member: discord.Member, *, reason: str = None):
        check = self.check_hierarchy(ctx, member)
        if check:
            return await ctx.send(check)
        try:
            await member.ban(reason=reason)
        except discord.Forbidden:
            return await ctx.send("I don't have the required permissions to ban this user.")
        except discord.HTTPException:
            return await ctx.send("I couldn't ban this user.")
        else:
            return await ctx.send(f"{member.mention} has been banned.")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context[Dandelion], member: discord.Member, *, reason: str = None):
        check = self.check_hierarchy(ctx, member)
        if check:
            return await ctx.send(check)
        try:
            await member.ban(reason=reason)
        except discord.Forbidden:
            return await ctx.send("I don't have the required permissions to ban this user.")
        except discord.HTTPException:
            return await ctx.send("I couldn't ban this user.")
        else:
            return await ctx.send(f"{member.mention} has been banned.")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context[Dandelion], *, member: discord.User):
        try:
            await ctx.guild.unban(member)
        except discord.NotFound:
            return await ctx.send("This user is not banned.")

    @commands.group(name="purge", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context[Dandelion], amount: int):
        if amount < 1:
            return await ctx.send("You must delete at least one message.")
        await ctx.channel.purge(limit=amount)
        return await ctx.send(f"Deleted {amount} messages.")

    @purge.command(name="user")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge_user(self, ctx: commands.Context[Dandelion], member: discord.Member, amount: int):
        if amount < 1:
            return await ctx.send("You must delete at least one message.")
        await ctx.channel.purge(limit=amount, check=lambda m: m.author == member)
        return await ctx.send(f"Deleted {amount} messages from {member.mention}.")

    @purge.command(name="regex")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge_regex(self, ctx: commands.Context[Dandelion], pattern: str, amount: int):
        if amount < 1:
            return await ctx.send("You must delete at least one message.")
        await ctx.channel.purge(limit=amount, check=lambda m: re.search(pattern, m.content))
        return await ctx.send(f"Deleted {amount} messages matching {pattern}.")

    @purge.command(name="dandelion")
    @commands.has_permissions(manage_messages=True)
    async def purge_self(self, ctx: commands.Context[Dandelion], amount: int):
        if amount < 1:
            return await ctx.send("You must delete at least one message.")
        await ctx.channel.purge(limit=amount, check=lambda m: m.author == ctx.guild.me, bulk=False)
        return await ctx.send(f"Deleted {amount} messages of the bot.")

    @purge.command(name="bot")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge_bot(self, ctx: commands.Context[Dandelion], amount: int):
        if amount < 1:
            return await ctx.send("You must delete at least one message.")
        await ctx.channel.purge(limit=amount, check=lambda m: m.author.bot)
        return await ctx.send(f"Deleted {amount} messages from bots.")

    


    



async def setup(bot: Dandelion):
    await bot.add_cog(Moderation(bot))
