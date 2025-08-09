
class TokenCountingError(Exception):
    """
    Custom exception for token counting errors.
    Attributes:
        value -- the value that caused the error
        message -- explanation of the error
    """

    def __init__(self, value, message: str = "Token counting error occurred"):
        super().__init__(message)
        self.value = value
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.value}"

class AisertError(Exception):
    """
    Base exception class for Aisert.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"AisertException: {self.message}"
