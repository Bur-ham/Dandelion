from discord.ext import commands

class DandelionException(Exception):
    """Base class for all Dandelion exceptions."""
    pass

class InvalidTimestampError(DandelionException):
    """Raised when a timestamp is invalid."""
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)
class UnguildedCommandUsage(commands.CheckFailure):
    """Base class for all Discord exceptions."""
    def __init__(self, message: str) -> None:
        self.message = message

class RequestException(DandelionException):
    """Base class for all request exceptions."""
    def __init__(self, code: int, message: str):
        self.message = message
        self.code = code
        super().__init__(message)

    def __str__(self):
        return self.message