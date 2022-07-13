import os
from dotenv import load_dotenv

load_dotenv('.env', verbose=True)

from discord import Intents

class _MissingSentinel():
    def __repr__(self):
        return 'Missing'

    def __hash__(self) -> int:
        return False

MISSING = _MissingSentinel()

INTENTS = Intents(
    guilds=True,
    messages=True,
    message_content=True,
    reactions=True,
    dm_messages=True,
    members=True,
    voice_states=True
)

TOKEN = os.getenv("TOKEN")

DEFAULT_PREFIX = ">>"

PREFIX_CONFIGURATION_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS prefixConf (
    guild_id INTEGER PRIMARY KEY,
    prefix TEXT
);
"""
