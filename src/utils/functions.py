from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Message

from src.models.cache import Cache
from .consts import DEFAULT_PREFIX, MISSING

if TYPE_CHECKING:
    from src.models.bot import Dandelion


async def get_prefix(bot: Dandelion, message: Message) -> str:
    db = bot.database.get_connection('config')
    if message.guild:
        cache = bot.cache.get(message.guild.id)
        if cache and cache.prefix != MISSING:
            return cache.prefix
        elif cache and cache.prefix == MISSING:
            return DEFAULT_PREFIX
        else:
            async with db.execute('SELECT prefix FROM prefixConf WHERE guild_id = ?', (message.guild.id,)) as cursor:
                prefix = await cursor.fetchone()
                if prefix is None:
                    bot.cache[message.guild.id] = Cache(prefix=MISSING)
                    return DEFAULT_PREFIX
                else:
                    prefix = [prefix[0] async for prefix in cursor]
                    bot.cache[message.guild.id] = Cache(prefix=prefix)
                    return prefix
    return DEFAULT_PREFIX
