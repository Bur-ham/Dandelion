class DandelionException(Exception):
    """Base class for all Dandelion exceptions."""
    pass

class RequestException(DandelionException):
    def __init__(self, code: int, message: str):
        self.message = message
        self.code = code
        super().__init__(message)

    def __str__(self):
        return self.message