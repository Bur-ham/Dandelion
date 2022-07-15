from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import aiosqlite
from src.utils.consts import PREFIX_CONFIGURATION_TABLE_SCHEMA

if TYPE_CHECKING:
    from src.models.bot import Dandelion

class Database:
    def __init__(self, bot: Dandelion) -> None:
        self.bot = bot
        self.connections: Dict[str, aiosqlite.Connection] = {}

    async def add_connection(self, name: str, filepath: str) -> None:
        self.connections[name] = await aiosqlite.connect(filepath, loop=self.bot.loop)
    
    def get_connection(self, name: str) -> aiosqlite.Connection:
        return self.connections[name]

    async def close_connection(self, name: str = None) -> None:
        if name:
            return self.connections.pop(name).close()
        for connection in self.connections.values():
            await connection.close()

    async def commit(self):
        for connection in self.connections.values():
            await connection.commit()

    async def create_tables(self):
        config = self.get_connection('config')
        await config.execute(PREFIX_CONFIGURATION_TABLE_SCHEMA)

        await self.commit()

    async def __aenter__(self) -> 'Database':
        await self.add_connection('config', 'database/config.db')
        await self.create_tables()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.commit()
        await self.close_connection()

    def __repr__(self) -> str:
        return f'<Database {self.db}>'
