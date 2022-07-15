from __future__ import annotations

import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from src.models.bot import Dandelion

class Fun(commands.Cog):
    def __init__(self, bot: Dandelion):
        self.bot = bot
        self.kawaii_red_api = os.getenv("KAWAII_RED_API")

    async def get_asset(self, type_: str, endpoint: str):
        base_api = "https://kawaii.red/api/{type_}/{endpoint}/token={token}".format(
            token=self.kawaii_red_api,
            type_=type_,
            endpoint=endpoint
        )
        json = await self.bot.session.get(base_api)
        return json['response']

    @commands.command(name="cuddle")
    async def cuddle(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "cuddle")
        embed = discord.Embed(
            description=f"{ctx.author.mention} cuddled {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="pat")
    async def pat(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "pat")
        embed = discord.Embed(
            description=f"{ctx.author.mention} patted {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="hug")
    async def hug(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "hug")
        embed = discord.Embed(
            description=f"{ctx.author.mention} hugged {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="kiss")
    async def kiss(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "kiss")
        embed = discord.Embed(
            description=f"{ctx.author.mention} kissed {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="slap")
    async def slap(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "slap")
        embed = discord.Embed(
            description=f"{ctx.author.mention} slapped {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="poke")
    async def poke(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "poke")
        embed = discord.Embed(
            description=f"{ctx.author.mention} poked {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)
    
    @commands.command(name="bite")
    async def bite(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "bite")
        embed = discord.Embed(
            description=f"{ctx.author.mention} bit {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)
    
    @commands.command(name="punch")
    async def punch(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "punch")
        embed = discord.Embed(
            description=f"{ctx.author.mention} punched {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="blush")
    async def blush(self, ctx: commands.Context[Dandelion]):
        asset = await self.get_asset("gif", "blush")
        embed = discord.Embed(
            description=f"{ctx.author.mention} blushed",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="cry")
    async def cry(self, ctx: commands.Context[Dandelion]):
        asset = await self.get_asset("gif", "cry")
        embed = discord.Embed(
            description=f"{ctx.author.mention} is crying",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)

    @commands.command(name="kill")
    async def kill(self, ctx: commands.Context[Dandelion], member: discord.Member):
        asset = await self.get_asset("gif", "kill")
        embed = discord.Embed(
            description=f"{ctx.author.mention} brutally killed {member.mention}",
            color=0xFF0000
        )
        embed.set_image(url=asset)
        return await ctx.send(embed=embed)


async def setup(bot: Dandelion):
    await bot.add_cog(Fun(bot))
    