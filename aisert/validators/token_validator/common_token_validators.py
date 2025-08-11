from typing import Dict, List
from .token_validator_base import TokenValidatorBase
from ...exception import TokenCountingError


class OpenAITokenValidator(TokenValidatorBase):
    """
    A token counter for OpenAI models.
    """

    _instances = {}

    def __init__(self, token_model, token_encoding):
        super().__init__(model_provider="openai")
        self.token_model = token_model
        self.token_encoding = token_encoding

    @classmethod
    def get_instance(cls, token_model: str = None, token_encoding: str = None):
        instance = None
        if not token_encoding and not token_model:
            raise ValueError("Either token_encoding or token_model must be provided.")

        key = token_encoding or token_model
        if key not in cls._instances:
            cls._instances[key] = cls(token_model, token_encoding)
        return cls._instances[key]

    def _get_encoding(self):
        """
        Returns the encoding for the specified encoding name.
        :return: The encoding object.
        """
        import tiktoken

        try:
            if self.token_encoding:
                self.logger.info(f"Using token encoding: {self.token_encoding}")
                try:
                    if self.token_encoding not in tiktoken.list_encodings():
                        self.logger.error(
                            f"Encoding {self.token_encoding} not found. Defaulting to best-for-model encoding."
                        )
                    else:
                        return tiktoken.get_encoding(self.token_encoding)
                except Exception as e:
                    self.logger.error(
                        f"Failed to get encoding for {self.token_encoding}: {e}"
                    )
                    self.logger.info("Defaulting to best-for-model encoding.")
            return tiktoken.encoding_for_model(self.token_model)
        except Exception as e:
            raise TokenCountingError(
                self.token_model, f"Failed to get tiktoken encoding_for_model: {e}"
            )

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
            raise TokenCountingError(
                self.token_model,
                f"Failed to count tokens for model {self.token_model}: {e}",
            )


class HuggingFaceTokenValidator(TokenValidatorBase):
    """
    A token counter for Hugging Face models.
    """

    _instances = {}

    def __init__(self, token_model):
        super().__init__(model_provider="huggingface")
        self.token_model = token_model

    @classmethod
    def get_instance(cls, token_model: str = None):
        """
        Get an instance of HuggingFaceTokenValidator with the specified token model.
        :param token_model: The model to use for token counting.
        :return: An instance of HuggingFaceTokenValidator.
        """
        if not token_model:
            raise TokenCountingError("token_model must be provided.")

        if token_model not in cls._instances:
            cls._instances[token_model] = cls(token_model)

        return cls._instances[token_model]

    def _get_encoding(self):
        """
        Returns the encoding for the specified token model.
        :return: The encoding object.
        """
        from transformers import AutoTokenizer

        try:
            self.logger.info(f"Using token model: {self.token_model}")
            tokenizer = AutoTokenizer.from_pretrained(self.token_model)
            return tokenizer
        except Exception as e:
            raise TokenCountingError(
                self.token_model, f"Failed to get AutoTokenizer: {e}"
            )

    def count(self, text):
        try:
            token_length = len(self._get_encoding().encode(text))
            self.logger.info(f"Token size is {token_length}.")
            return token_length
        except Exception as e:
            raise TokenCountingError(
                self.token_model,
                f"Failed to load tokenizer for model {self.token_model}: {e}",
            )


class AnthropicTokenValidator(TokenValidatorBase):
    """
    A token counter for Anthropic models.
    """

    _instances = {}

    def __init__(self, token_model):
        super().__init__(model_provider="anthropic")
        self.token_model = token_model

    @classmethod
    def get_instance(cls, token_model: str = None):
        """
        Get an instance of AnthropicTokenValidator with the specified token model.
        :param token_model: The model to use for token counting.
        :return: An instance of AnthropicTokenValidator.
        """
        if not token_model:
            raise TokenCountingError("token_model must be provided.")

        if token_model not in cls._instances:
            cls._instances[token_model] = cls(token_model)

        return cls._instances[token_model]

    def _get_encoding(self):
        """
        Returns the encoding for the specified token model.
        :return: The encoding object.
        """
        import anthropic

        try:
            return anthropic.Client()
        except Exception as e:
            raise TokenCountingError(
                self.token_model, f"Failed to get anthropic client: {e}"
            )

    def count(self, text: List[Dict]):
        """
        Counts the number of tokens in the provided text.
        :param text: The input text to count tokens from, expected to be a list of message dictionaries.
        :return: The number of tokens in the text.
        """

        if not (
                isinstance(text, list) and all(isinstance(item, dict) for item in text)
        ):
            raise TokenCountingError(
                self.token_model, "Text must be a list of message dictionaries."
            )
        try:
            token_length = self._get_encoding().count_tokens(
                model=self.token_model, messages=text
            )
            self.logger.info(f"Token size is {token_length}.")
            return token_length
        except Exception as e:
            raise TokenCountingError(
                self.token_model,
                f"Failed to count tokens for model {self.token_model}: {e}",
            )


class GoogleTokenValidator(TokenValidatorBase):
    """
    A token counter for Google models.
    """

    _instances = {}

    def __init__(self, token_model):
        super().__init__(model_provider="google")
        self.token_model = token_model

    @classmethod
    def get_instance(cls, token_model: str = None):
        """
        Get an instance of GoogleTokenValidator with the specified token model.
        :param token_model: The model to use for token counting.
        :return: An instance of GoogleTokenValidator.
        """
        if not token_model:
            raise TokenCountingError("token_model must be provided.")
        if token_model not in cls._instances:
            cls._instances[token_model] = cls(token_model)
        return cls._instances[token_model]

    def _get_encoding(self):
        """
        Returns the encoding for the specified encoding name.
        :return: The encoding object.
        """
        try:
            from google import genai

            return genai.Client()
        except Exception as e:
            raise TokenCountingError(
                self.token_model, f"Failed to get google genai client: {e}"
            )

    def count(self, text):
        """
        Counts the number of tokens in the provided text.
        :param text: The input text to count tokens from.
        :return: The number of tokens in the text.
        """
        try:
            token_length = self._get_encoding().count_tokens(
                text, model=self.token_model
            )
            self.logger.info(f"Token size is {token_length}.")
            return token_length
        except Exception as e:
            raise TokenCountingError(
                self.token_model,
                f"Failed to count tokens for model {self.token_model}: {e}",
            )
