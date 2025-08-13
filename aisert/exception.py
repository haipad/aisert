class TokenCountingError(Exception):
    """
    Custom exception for token counting errors.
    Attributes:
        value -- the value that caused the error
        message -- explanation of the error
    """

    def __init__(self, value="", message="Token counting error"):
        super().__init__(message)
        self.value = value

    def __str__(self):
        return f"{self.args[0]}: {self.value}"


class AisertError(Exception):
    """Base exception class for Aisert."""

    def __str__(self):
        return f"AisertError: {self.args[0]}"