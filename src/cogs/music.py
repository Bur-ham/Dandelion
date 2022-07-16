from __future__ import annotations

import os
from asyncio import QueueFull
from typing import TYPE_CHECKING, Dict, Union


import discord
import wavelink
from wavelink.ext import spotify
from discord.ext import commands

from src.models.errors import InvalidTimestampError, UnguildedCommandUsage
from src.models.music import MusicQueue

if TYPE_CHECKING:
    from src.models.bot import Dandelion


class Music(commands.Cog):
    def __init__(self, bot: Dandelion) -> None:
        self.bot = bot
        self.active_players: Dict[int, MusicQueue] = {}
        self.spotify_credentials = (
            os.getenv("SPOTIFY_CLIENT_ID"),
            os.getenv("SPOTIFY_CLIENT_SECRET")
        )

    def create_embed(
        self, 
        user: discord.Member, 
        track: Union[spotify.SpotifyTrack, wavelink.YouTubeTrack, wavelink.PartialTrack]
    ) -> discord.Embed:
        if isinstance(track, wavelink.PartialTrack):
            embed = discord.Embed(title="Now Playing", description=track.title, color=0x00ff00)
            
        else:
            embed = discord.Embed(title="Now playing", description=f"{track.title} by {track.author}", color=0x00ff00)
            embed.set_thumbnail(url=track.thumbnail)

        embed.set_footer(text=f"Requested by {user.display_name}", icon_url=user.avatar.url)
        return embed

    def convert_timestamp(self, timestamp: str) -> int:
        times = timestamp.split(':')
        print(times)
        try:
            if len(times) == 2:
                return int(times[0]) * 60 + int(times[1])
            elif len(times) == 3:
                return int(times[0]) * 3600 + int(times[1]) * 60 + int(times[2])
            elif len(times) == 4:
                return int(times[0]) * 86400 + int(times[1]) * 3600 + int(times[2]) * 60 + int(times[3])
            else:
                raise InvalidTimestampError("Invalid timestamp was provided")
        except ValueError:
            raise InvalidTimestampError("Invalid timestamp was provided")
        


    async def cog_load(self) -> None:
        id_, secret = self.spotify_credentials
        if id_ and secret:
            node = await wavelink.NodePool.create_node(
                bot=self.bot,
                host='0.0.0.0',
                port=2333,
                password='youshallnotpass',
                spotify_client=spotify.SpotifyClient(client_id=id_, client_secret=secret)
            )
        else:
            node = await wavelink.NodePool.create_node(
                bot=self.bot,
                host='0.0.0.0',
                port=2333,
                password='youshallnotpass'
            )

    async def cog_before_invoke(self, ctx: commands.Context[Dandelion]) -> None:
        if not ctx.guild:
            raise UnguildedCommandUsage("This command can only be used in a server.")
        if ctx.guild.voice_client is None and ctx.author.voice:
            try:
                await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except discord.ClientException:
                return await ctx.send("I couldn't connect to your voice channel.")
            else:
                return await ctx.send(f"Connected to {ctx.author.voice.channel.mention}")
        elif ctx.guild.voice_client is not None and ctx.author.voice:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send("You must be in the same voice channel as the bot.")
            else:
                return True

    def register_or_get_player(self, ctx: commands.Context[Dandelion]) -> MusicQueue:
        if ctx.guild.id not in self.active_players:
            self.active_players[ctx.guild.id] = MusicQueue(200)
        return self.active_players[ctx.guild.id]

    @commands.group(name="play", invoke_without_command=True)
    async def play(
        self, 
        ctx: commands.Context[Dandelion], 
        *, 
        query: wavelink.YouTubeTrack
    ) -> None:
        print(query)
        vc: wavelink.Player = ctx.voice_client
        if vc:
            if vc.is_playing():
                player = self.register_or_get_player(ctx)
                try:
                    player.put((ctx.channel.id, ctx.author.id, query))
                except QueueFull:
                    return await ctx.send("Queue is full.")
                return await ctx.send(f"{query.title} has been Added to queue. {player.qsize()}/{player.max_size} tracks in queue currently.")
            else:
                embed = self.create_embed(ctx.author, query)
                await vc.play(query)
                return await ctx.send(embed=embed)

    @play.command(name="spotify")
    async def play_spotify(self, ctx: commands.Context[Dandelion], *, query: str) -> None:
        vc: wavelink.Player = ctx.voice_client
        if vc:
            queue = self.register_or_get_player(ctx)
            count = 0
            async for partial in spotify.SpotifyTrack.iterator(query=query, partial_tracks=True):
                try:
                    queue.put((ctx.channel.id, ctx.author.id, partial))
                except QueueFull:
                    break
                count += 1
            if count == 0:
                return await ctx.send("Queue is full.")
            await ctx.send(f"Added {count} entries to queue. {queue.qsize()}/{queue.max_size} tracks in queue currently.")
            if vc.is_playing():
                pass
            else:
                _, _, track = queue.get()
                embed = self.create_embed(ctx.author, track)
                await vc.play(track)
                return await ctx.send(embed=embed)


    @commands.command(name="pause")
    async def pause(self, ctx: commands.Context[Dandelion]) -> None:
        vc: wavelink.Player = ctx.voice_client
        if vc:
            if vc.is_playing():
                await vc.pause()
                embed = discord.Embed(title="Paused", color=0x00ff00)
                embed.description = "The music has been paused."
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Nothing is playing")
        
    @commands.command(name="resume")
    async def resume(self, ctx: commands.Context[Dandelion]) -> None:
        vc: wavelink.Player = ctx.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
                embed = discord.Embed(title="Resumed", color=0x00ff00)
                embed.description = "The music has been resumed."
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Nothing is paused")

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context[Dandelion]) -> None:
        vc: wavelink.Player = ctx.voice_client
        if vc:
            if vc.is_playing():
                await vc.stop() 
                embed = discord.Embed(title="Stopped", color=0x00ff00)
                embed.description = "The music has been stopped."
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Nothing is playing")
    
    @commands.command(name="skip")
    async def skip(self, ctx: commands.Context[Dandelion]) -> None:
        vc: wavelink.Player = ctx.voice_client
        if vc:
            if vc.is_playing():
                await vc.stop()
                embed = discord.Embed(title="Skipped", color=0x00ff00)
                embed.description = "The music has been skipped."
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Nothing is playing")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason) -> None:
        print(f"Track {track.title} ended. Reason: {reason}")
        if player.guild.id in self.active_players:
            queue = self.active_players[player.guild.id]
            if not queue.empty():
                channel_id, user_id, track = queue.get()
                user = player.guild.get_member(user_id)
                channel = player.guild.get_channel(channel_id)
                embed = self.create_embed(user, track)
                await channel.send(embed=embed)
                await player.guild.voice_client.play(track)

    @commands.command()
    async def seek(self, ctx: commands.Context[Dandelion], time: Union[int, str]) -> None:
        vc: wavelink.Player = ctx.voice_client
        if vc:
            if vc.is_playing():
                if isinstance(time, int):
                    await vc.seek(time * 1000)
                    embed = discord.Embed(title="Seeked", color=0x00ff00)
                    embed.description = f"The music has been seeked to {time} seconds."
                    return await ctx.send(embed=embed)
                else:
                    try:
                        time_sec = self.convert_timestamp(time) * 1000
                    except InvalidTimestampError:
                        return await ctx.send("Invalid timestamp was provided")
                    await vc.seek(time_sec)
                    embed = discord.Embed(title="Seeked", color=0x00ff00)
                    embed.description = f"The music has been seeked to {time}"
            else:
                return await ctx.send("Nothing is playing")


    @commands.command(name="queue")
    async def queue(self, ctx: commands.Context[Dandelion]) -> None:
        if ctx.guild.id in self.active_players:
            queue = self.active_players[ctx.guild.id]
            if queue.empty():
                return await ctx.send("Queue is empty.")
            else:
                embeds = []
                for i in range(0, queue.qsize(), 10):
                    embed = discord.Embed(title="Queue", color=0x00ff00)
                    embed.set_footer(text=f"{queue.qsize()}/{queue.max_size} tracks in queue currently.")
                    for j in range(10):
                        try:
                            _, user_id, track = queue[i+j-1]
                        except IndexError:
                            break
                        user = ctx.guild.get_member(user_id) 
                        embed.add_field(name=f"{i+j+1}. {track.title}", value=f"Requested by {user.display_name}", inline=False)
                    embeds.append(embed)
                await ctx.send(embed=embeds[0])
        else:
            return await ctx.send("Queue is empty.")

    

    @play.before_invoke
    async def before_play(self, ctx: commands.Context[Dandelion]) -> None:
        if ctx.guild.id in self.active_players:
            return
        else:
            self.active_players[ctx.guild.id] = MusicQueue(200)


async def setup(bot: Dandelion) -> None:
    await bot.add_cog(Music(bot))
