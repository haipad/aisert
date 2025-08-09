import logging
from typing import List, Optional

from .exception import AisertError

from .config.config import AIsertConfig
from .models.result import AisertStatus
from .validators.contains_validator import ContainsValidator
from .validators.schema_validator import SchemaValidator
from .validators.semantic_validator import SemanticValidator
from .validators.token_validator.token_validator import TokenValidator
from .utils.print_util import PrintUtil as pu


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

    def __init__(self, content: str, config: Optional[AIsertConfig] = None):
        """
        Initializes the Aisert instance with the provided content.
        :param content: The content to be validated. Expected to be a LLM response string.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.content = content
        self.status = AisertStatus()
        self._configure(config)
    
    def _configure(self, config):
        """
        Configures the Aisert instance with the provided configuration.
        :param config: Configuration for Aisert, can be an AIsertConfig instance, a dictionary, or a path to a configuration file.
        """

        self.logger.debug(f"Configuring Aisert with config: {pu.sanitize_text(type(config).__name__)}")
        
        if isinstance(config, AIsertConfig):
            self.config = config
        elif type(config) is str:
            self.config = AIsertConfig.load(config)
        else:
            self.config = AIsertConfig.get_default_config()     

    def assert_schema(self, schema, strict: bool = True):
        """
        Asserts that the content matches the provided schema.
        :param schema: The schema to validate against.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the schema validation.
        """
        self.schema_validator = SchemaValidator()
        self.logger.debug(f"Checking if content is matching {pu.sanitize_text(schema)}")
        result = self.schema_validator.validate(self.content, schema)
        self.status.update(self.schema_validator.name, result)
        if strict and not result.status:
            raise AisertError(f"{result.reason}")
        self.logger.debug(f"Schema validation result: {result.status} - {pu.sanitize_text(result.reason)}")
        return self

    def assert_contains(self, items: List[str], strict: bool = True):
        """
        Asserts that the content contains the specified items.
        :param items: A list of items to check for in the content.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the containment validation.
        """
        self.contains_validator = ContainsValidator()
        self.logger.debug(f"Checking if content contains {pu.sanitize_text(items)}")
        result = self.contains_validator.validate(self.content, items)
        self.status.update(self.contains_validator.name, result)
        if strict and not result.status:
            raise AisertError(f"{result.reason}")
        self.logger.debug(f"Contains validation result: {result.status} - {pu.sanitize_text(result.reason)}")
        return self

    def assert_tokens(self, size:int, strict: bool = True):
        """
        Asserts that the number of tokens in the content is less than the specified size.
        :param size: The maximum number of tokens allowed.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the token validation.
        """
        self.token_validator = TokenValidator(model_provider=self.config.model_provider)
        self.logger.debug(f"Checking if tokens less than: {pu.sanitize_text(size)}")
        result = self.token_validator.validate(
            self.content, token_limit=size, token_model=self.config.token_model, token_encoding=self.config.token_encoding
        )
        self.status.update(self.token_validator.name, result)
        if strict and not result.status:
            raise AisertError(f"{result.reason}")
        self.logger.debug(f"Token validation result: {result.status} - {pu.sanitize_text(result.reason)}")
        return self

    def assert_semantic_matches(self, other, strict: bool = True):
        """
        Asserts that the semantic content of this instance matches other text.
        :param other: Other text to compare against.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the semantic validation.
        """
        self.semantic_validator = SemanticValidator(model_name=self.config.sentence_transformer_model)
        self.logger.debug(f"Checking semantic match")
        result = self.semantic_validator.validate(self.content, other)
        self.status.update(self.semantic_validator.name, result)
        if strict and not result.status:
            raise AisertError(f"{result.reason}")
        self.logger.debug(f"Semantic validation result: {result.status} - {pu.sanitize_text(result.reason)}")
        return self

    def collect(self):
        """
        Collects the results of all validations performed on this instance.
        :return: A dictionary containing the validation results.
        """
        results = {
            "status" : all(v.status for v in self.status.collect().values()),
            "rules": {}
        }
        for k, v in self.status.collect().items():
            results["rules"][k] = v.to_dict()
        return results
