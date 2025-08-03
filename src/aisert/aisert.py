import logging
from typing import List

from src.config.config import AIsertConfig
from src.modules.schema_validator import SchemaValidator
from src.modules.semantic_validator import SemanticMatch
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
        self.content = content
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

    def configure(self, config):
        """
        Configures the Aisert instance with the provided configuration.
        :param config: An instance of AIsertConfig or a file_path with configuration settings.
        """

        self.logger.debug(f"Configuring {self.name} with {self.config}")

        if isinstance(config, AIsertConfig):
            self.config = config
        elif isinstance(config, dict):
            self.config = AIsertConfig.load_from_json(config)
        else:
            self.config = AIsertConfig.get_default_config()
        self.token_counter = TokenValidator()
        self.semantic_matcher = SemanticMatch()

    def assert_schema(self, schema):
        self.logger.debug(f"Checking if contnt is matching {schema}")
        assert SchemaValidator.is_schema_match(self.content, schema), "Content does not match schema"
        return self

    def assert_contains(self, items: List[str]):
        self.logger.debug(f"Checking if content contains {items}")
        assert item in self.content, f"Content does not contain {item}"
        return self

    def assert_tokens_less_than(self, size):
        self.logger.debug(f"Checking if {self.name} has tokens less than: {size}")
        assert self.token_counter.count_tokens() < size, f"Token count is not less than {size}"
        return self

    def assert_tokens_greater_than(self, size):
        self.logger.debug(f"Checking if {self.name} has tokens greater than: {size}")
        assert self.token_counter.count_tokens() > size, f"Token count is not greater than {size}"
        return self

    def assert_semantic_equals(self, other):
        self.logger.debug(
            f"Checking semantic equality between {self.name} and {other.name}"
        )
        assert self.semantic_matcher.compare(self.content, other.content), "Other must be an instance of Aisert"
        return self
