

from src.modules.validator import BaseValidator


class TokenValidatorBase:

    def __init__(self, model_provider: str = None):
        super().__init__()
        self.mode_provider = model_provider

    
    def count(self, text: str) -> int:
        """
        Not implemented error.
        This method should be overridden in subclasses to count tokens in the provided text.
        """
        raise NotImplementedError("Subclasses must implement the count method.")
