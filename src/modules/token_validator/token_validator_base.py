

from src.modules.validator import BaseValidator


class TokenValidatorBase:

    def __init__(self, model_provider: str = None):
        super().__init__()
        self.model_provider = model_provider
    
    def get_model_provider(self):
        """
        Returns the model provider for the token validator.
        
        :return: The model provider string.
        """
        return self.model_provider
    
    def _get_encoding(self):
        """
        Returns the encoding client for the specified encoding name.
        :return: The encoding client object.
        """
        raise NotImplementedError("Subclasses must implement the _get_encoding method.")

    @classmethod
    def get_instance(cls):
        """
        Returns an instance of the token validator.
        This method should be overridden in subclasses to return the appropriate instance.
        """
        raise NotImplementedError("Subclasses must implement the get_instance method.")
    
    def count(self, text: str) -> int:
        """
        Not implemented error.
        This method should be overridden in subclasses to count tokens in the provided text.
        """
        raise NotImplementedError("Subclasses must implement the count method.")
