import logging
from typing import List, Optional

from .models.report import AisertReport

from .exception import AisertError

from .config.config import AisertConfig
from .models.result import AisertStatus, Result
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

    def __init__(self, content: str, config: Optional[AisertConfig] = None):
        """
        Initializes the Aisert instance with the provided content.
        :param content: The content to be validated. Expected to be a LLM response string.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.content = content
        self.status = AisertStatus()
        self.config = config or AisertConfig.get_default_config()

    def assert_schema(self, schema, strict: bool = True):
        """
        Asserts that the content matches the provided schema.
        :param schema: The schema to validate against.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the schema validation.
        """
        self.logger.debug(f"Checking if content is matching {schema}")
        self._validate(SchemaValidator(), strict,self.content, schema)
        return self

    def assert_contains(self, items: List[str], strict: bool = True):
        """
        Asserts that the content contains the specified items.
        :param items: A list of items to check for in the content.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the containment validation.
        """
        self.logger.debug(f"Checking if content contains {items}")
        self._validate(ContainsValidator(), strict, self.content, items)
        return self

    def assert_tokens(self, size:int, strict: bool = True):
        """
        Asserts that the number of tokens in the content is less than the specified size.
        :param size: The maximum number of tokens allowed.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the token validation.
        """
        self.logger.debug(f"Checking if tokens less than: {size}")
        self._validate(TokenValidator(model_provider=self.config.model_provider), strict,
                       self.content, token_limit=size, token_model=self.config.token_model, token_encoding=self.config.token_encoding
        )
        return self

    def assert_semantic_matches(self, other, threshold: float = 0.8, strict: bool = True):
        """
        Asserts that the semantic content of this instance matches other text.
        :param other: Other text to compare against.
        :param strict: If True, raises AisertError on validation failure.
        :return: The result of the semantic validation.
        """
        self.logger.debug(f"Checking semantic match")
        self._validate(SemanticValidator.get_instance(model_name=self.config.sentence_transformer_model),
                       strict, self.content, other, threshold)
        return self

    def _validate(self, validator, strict, *args, **kwargs):
        """
        Calls the validate method of validator and updates result.
        :param validator: The validator instance.
        :param args: Positional arguments for the validator.
        :param kwargs: Keyword arguments for the validator.
        """
        try:
            result = validator.validate(*args, **kwargs)
            self.logger.debug(f"{validator.name} validation result: {result.status}")
        except AisertError as e:
            if strict:
                self.logger.error(f"{validator.name} validation failed")
                raise
            else:
                self.logger.error(f"{validator.name} validation failed: {str(e)}")
                result = Result(status=False, reason=str(e))
        self.status.update(validator.name, result)

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
        return AisertReport(**results)