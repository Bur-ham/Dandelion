from dataclasses import dataclass
from typing import Union

from src.utils.consts import _MissingSentinel


@dataclass(slots=True, repr=True, kw_only=True)
class Cache:
    prefix: Union[list[str], _MissingSentinel]
    commands_executed: int = 0