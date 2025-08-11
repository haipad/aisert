from typing import Any
from pydantic import BaseModel, TypeAdapter, ValidationError

from .validator import BaseValidator
from ..models.result import Result


class SchemaValidator(BaseValidator):
    """
    A class to validate content against a schema.
    """

    def __init__(self):
        super().__init__("SchemaValidator")

    def validate(self, content: Any, schema: Any):
        """
        Validates if the content matches the schema.

        :param content: The content to validate.
        :param schema: The schema to validate against.
        :return: Result true/false with reason.
        """
        self.logger.debug(f"Validating content against schema: {schema}")
        
        if (isinstance(schema, type) and issubclass(schema, BaseModel)) or (hasattr(schema, "__origin__")):
            try:
                TypeAdapter(schema).validate_python(content)
                return Result(True, "")
            except ValidationError as e:
                return Result(False, str(e))
        return Result(False, "Provided schema is not a valid Pydantic model")