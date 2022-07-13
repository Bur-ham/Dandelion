from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from src.models.bot import Dandelion


class Moderation(commands.Cog):
    def __init__(self, bot: Dandelion):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context[Dandelion]) -> bool:
        permissions = ['manage_messages', 'manage_guild', 'kick_members', 'ban_members', 'manage_roles']
        if not ctx.guild:
            return False
        elif not any(getattr(ctx.author.guild_permissions, perm) for perm in permissions):
            return False
        else:
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

async def setup(bot: Dandelion):
    await bot.add_cog(Moderation(bot))