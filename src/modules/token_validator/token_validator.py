from typing import override

from src.modules.token_validator.token_validator_base import TokenValidatorBase

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


class OpenAITokenValidator(TokenValidatorBase):
    """
    A token counter for OpenAI models.
    """
    def __init__(self, token_model: str=None, token_encoding: str=None):
        if not token_encoding and not token_model:
            raise ValueError("Either token_encoding or token_model must be provided.")
        super().__init__(model_provider="openai")
        self.token_model = token_model
        self.token_encoding = token_encoding

    def _get_encoding(self):
        """
        Returns the encoding for the specified encoding name.
        :param encoding_name: The name of the encoding to retrieve.
        :return: The encoding object.
        """
        import tiktoken
        try:
            if self.token_encoding:
                self.logger.info(f"Using token encoding: {self.token_encoding}")
                try:
                    if self.token_encoding not in tiktoken.list_encodings():
                        self.logger.error(f"Encoding {self.token_encoding} not found. Defaulting to best-for-model encoding.")
                    else:
                        self.encoding = tiktoken.get_encoding(self.token_encoding)
                        return self.encoding
                except Exception as e:
                    self.logger.error(f"Failed to get encoding for {self.token_encoding}: {e}")
                    self.logger.info("Defaulting to best-for-model encoding.")
            self.encoding = tiktoken.encoding_for_model(self.token_model)
        except Exception as e:
            raise TokenCountingError(self.token_model, f"Failed to load tokenizer for model {self.token_model}: {e}")
        return self.encoding
    
    @override
    def count(self, text):
        """
        Counts the number of tokens in the provided text.
        :param text: The input text to count tokens from.
        :return: The number of tokens in the text.
        """
        try:
            token_length = len(self._get_encoding().encode(text))
            self.logger.info(f"Token size is {token_length}.")
            return token_length
        except Exception as e:
            raise TokenCountingError(self.token_model, f"Failed to count tokens for model {self.token_model}: {e}")


class HuggingFaceTokenValidator(TokenValidatorBase):
    """
    A token counter for Hugging Face models.
    """
    def __init__(self, token_model: str=None):
        if not token_model:
            raise TokenCountingError("token_model must be provided.")
        super().__init__(model_provider="huggingface")
        self.token_model = token_model
    
    @override
    def count(self, text):
        from transformers import AutoTokenizer
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.token_model)
            token_length = len(tokenizer.encode(text))
            self.logger.info(f"Token size is {token_length}.")
        except Exception as e:
            raise TokenCountingError(self.token_model, f"Failed to load tokenizer for model {self.token_model}: {e}")
        return token_length
    


class AnthropicTokenValidator(TokenValidatorBase):
    """
    A token counter for Anthropic models.
    """
    def __init__(self, token_model: str=None, api_key: str = None):
        if not token_model:
            raise TokenCountingError("token_model must be provided.")
        super().__init__(model_provider="anthropic")
        self.token_model = token_model
        self.api_key = api_key
    
    @override
    def count(self, text):
        import anthropic
        try:
            client = anthropic.Client()
            token_length = client.count_tokens(model=self.token_model, messages=text)
            self.logger.info(f"Token size is {token_length}.")
        except Exception as e:
            raise TokenCountingError(self.token_model, f"Failed to count tokens for model {self.token_model}: {e}")
        return token_length
    

    
class GoogleTokenValidator(TokenValidatorBase):
    """
    A token counter for Google models.
    """
    def __init__(self, token_model: str=None):
        if not token_model:
            raise TokenCountingError("token_model must be provided.")
        super().__init__(model_provider="google")
        self.token_model = token_model

    @override
    def get_encoding(self):
        """
        Returns the encoding for the specified encoding name.
        :return: The encoding object.
        """
        pass
    
    @override
    def count(self, text):
        """
        Counts the number of tokens in the provided text.
        :param text: The input text to count tokens from.
        :return: The number of tokens in the text.
        """
        try:
            from google import genai
            client = genai.Client()
            count = client.count_tokens(text, model=self.token_model)
            self.logger.info(f"Token size is {count}.")
            return count
        except Exception as e:
            raise TokenCountingError(self.token_model, f"Failed to count tokens for model {self.token_model}: {e}")
