from .token_validator_factory import TokenValidatorFactory
from ...exception import TokenCountingError
from ..validator import BaseValidator


class TokenValidator(BaseValidator):
    """
    Validates the number of tokens in a given text.
    """
    def __init__(self, model_provider: str = None):
        super().__init__("TokenValidator")
        self.model_provider = model_provider


    def validate(self, text, token_limit: int = 100, token_model: str = None, token_encoding: str = None):
        """
        Validates the number of tokens in the text.
        
        :param token_model: The model to use for token counting.
        :param token_encoding: The encoding to use for token counting.
        :return: The number of tokens in the text.
        """        
        try:          
            token_validator = TokenValidatorFactory.get_instance(
                model_provider=self.model_provider,
                token_model=token_model,
                token_encoding=token_encoding
            )
            token_count = token_validator.count(text)
            self.logger.debug(f"Token count: {token_count}")

            if token_count > token_limit:
                self.status = False
                self.reason = f"Token limit exceeded: {token_count} tokens found, limit is {token_limit}"
            else:
                self.status = True
                self.reason = f"Token count {token_count} is within limit {token_limit}"

        except (TokenCountingError, Exception) as e:
            self.logger.error(f"Error counting tokens: {e}")
            self.status = False
            self.reason = str(e)

        return self.result
