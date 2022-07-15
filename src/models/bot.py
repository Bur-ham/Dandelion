import datetime
import logging
import os
from typing import Dict

from discord.ext import commands
from src.models.cache import Cache
from src.models.http import HTTPClient
from src.utils.consts import INTENTS

from .database import Database
from .help import DandelionHelp


class Dandelion(commands.Bot): # can be switched to commands.AutoShardedBot
    def __init__(self, *args, **kwargs):
        help_ = DandelionHelp(
            command_attrs={
                'cooldown': commands.CooldownMapping.from_cooldown(1, 3, commands.BucketType.user),
                'help': 'Displays all commands or the help of a specific command.'
            }
        )
        super().__init__(intents=INTENTS, help_command=help_, *args, **kwargs)
        self.database: Database = None
        self.session: HTTPClient = None
        self.cache: Dict[int, Cache] = {}
        
    async def load_cogs(self):
        for cog in os.listdir('src/cogs'):
            if cog.endswith('.py'):
                name = cog[:-3]
                self.logger.info(f'Loading cog {name}')
                await self.load_extension(f'src.cogs.{name}')

    def create_self_logger(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
        self.logger = logging.getLogger("Dandelion")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='logs/runtime.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s: [%(levelname)s]     %(name)s: %(message)s'))
        self.logger.addHandler(handler)

    async def on_ready(self):
        self.create_self_logger()
        self.logger.info(f'Logged in as {self.user.name}')
        self.logger.info(f'Bot is ready.')

    async def setup_hook(self) -> None:
        self.create_self_logger()
        await self.load_cogs()
        return await super().setup_hook()

    async def fill_basic_cache(self) -> None:
        database = self.database.get_connection('config')
        async with database.execute('SELECT guild_id, prefix FROM prefixConf') as cursor:
            async for (guild_id, prefix) in cursor:
                if guild_id not in self.cache:
                    self.cache[guild_id] = Cache([prefix])
                else:
                    self.cache[guild_id].prefix.append(prefix)

    async def start(self, *args, **kwargs):
        async with HTTPClient() as self.session:
            async with Database(self) as db:
                self.database = db
                await self.fill_basic_cache()
                await super().start(*args, **kwargs)

    async def release_slash_commands(self):
        await self.tree.sync()
        time_now = datetime.datetime.utcnow()
        time_str = time_now.strftime('%Y-%m-%d %H:%M:%S')
        await self.logger.info(f'Slash commands released at {time_str}')
