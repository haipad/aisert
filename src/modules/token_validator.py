import tiktoken
import logging

from src.modules.validator import BaseValidator


class TokenValidator(BaseValidator):
    """
    A class to count tokens in a given text.
    This is a placeholder implementation and should be replaced with actual logic.
    """

    _instances = {}

    def __init__(self):
        super().__init__()
        self.encoding_name = "cl100k_base"
        self.encoding_model = "gpt-3.5-turbo"
        self.encoding = None

    def validate(self, text: str) -> int:
        """
        Count the number of tokens in the provided text.
        
        Args:
            text (str): The input text to count tokens from.
        
        Returns:
            int: The number of tokens in the text.
        """
        self.logger.info(f"Token size is {len(self.encoding.encode(text))}.")  # Log first 50 characters
        return len(self.encoding.encode(text))

    @staticmethod
    def get_instance(encoding_model: str=None, encoding_name: str = None):
        """
        Get an instance of TokenValidator with specified encoding.
        
        Args:
            encoding_name (str): The name of the encoding to use.
            encoding_model (str): The model for which the encoding is used.
        
        Returns:
            TokenValidator: An instance of TokenValidator.
        """
        if not encoding_model and not encoding_name:
            encoding_model = "gpt-3.5-turbo"

        if encoding_name not in TokenValidator._instances:
            if {"encoding_name": encoding_name, "encoding_model": encoding_model} in TokenValidator._instances:
                return TokenValidator._instances[{"encoding_name": encoding_name, "encoding_model": encoding_model}]
            
            TokenValidator._instances[encoding_name] = TokenValidator()
            TokenValidator._instances[encoding_name].encoding_name = encoding_name
            TokenValidator._instances[encoding_name].encoding_model = encoding_model
            TokenValidator._instances[encoding_name].encoding = tiktoken.get_encoding(encoding_name)
        
        return TokenValidator._instances[encoding_name]