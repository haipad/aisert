import logging
from typing import List

from src.config.config import AIsertConfig
from src.modules.contains_validator import ContainsValidator
from src.modules.schema_validator import SchemaValidator
from src.modules.semantic_validator import SemanticValidator
from src.modules.token_validator.token_validator import TokenValidator


class Aisert:
    """
    Aisert is a class that provides methods for configuration, schema assertion,
    containment checks, token size assertions, and semantic equality checks.
    It is designed to be flexible and can be extended with additional functionality
    as needed.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    def __init__(self, content):
        """
        Initializes the Aisert instance with the provided content.

        :param content: The content to be validated. Expected to be a string or relevant data structure.
        """
        self.content = content
        self.logger = logging.getLogger(self.__class__.__name__)

    def configure(self, config):
        """
        Configures the Aisert instance with the provided configuration.
        :param config: An instance of AIsertConfig, a dict, or a file_path with configuration settings.
        """

        self.logger.debug(f"Configuring with config type: {type(config).__name__}")

        if isinstance(config, AIsertConfig):
            self.config = config
        elif isinstance(config, dict):
            self.config = AIsertConfig(**config)
        elif isinstance(config, str):
            self.config = AIsertConfig.load(config)
        else:
            self.config = AIsertConfig.get_default_config()

        self.token_validator = TokenValidator(model_provider=self.config.model_provider)
        self.semantic_validator = SemanticValidator(model_name=self.config.sentence_transformer_model)
        self.schema_validator = SchemaValidator()
        self.contains_validator = ContainsValidator()

    def assert_schema(self, schema):
        """
        Asserts that the content matches the provided schema.
        :param schema: The schema to validate against.
        :return: The result of the schema validation.
        """
        self.logger.debug(f"Checking if content is matching {schema}")
        result = self.schema_validator.validate(self.content, schema)
        assert result.status, f"{result.reason}"
        return self

    def assert_contains(self, items: List[str]):
        """
        Asserts that the content contains the specified items.
        :param items: A list of items to check for in the content.
        :return: The result of the containment validation.
        """
        self.logger.debug(f"Checking if content contains {items}")
        result = self.contains_validator.validate(self.content, items)
        assert result.status, f"{result.reason}"
        return self

    def assert_tokens(self, size):
        """
        Asserts that the number of tokens in the content is less than the specified size.
        :param size: The maximum number of tokens allowed.
        :return: The result of the token validation.
        """
        self.logger.debug(f"Checking if tokens less than: {size}")
        result = self.token_validator.validate(
            self.content, token_limit=size, token_model=self.config.token_model, token_encoding=self.config.token_encoding
        )
        assert result.status, f"{result.reason}"
        return self

    def assert_semantic_matches(self, other):
        """
        Asserts that the semantic content of this instance matches other text.
        :param other: Other text to compare against.
        :return: The result of the semantic validation.
        """
        self.logger.debug(
            f"Checking semantic match between"
        )
        result = self.semantic_validator.validate(self.content, other)
        assert result.status, f"{result.reason}"
        return self
