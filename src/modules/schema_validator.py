import logging
from pydantic import BaseModel, ValidationError

from src.modules.validator import BaseValidator


class SchemaValidator(BaseValidator):
    """
    A class to validate content against a schema.
    """

    def __init__(self):
        """
        Initializes the SchemaValidator class.
        """
        super().__init__()

    def validate(self, content: dict, schema):
        """
        Validates if the content matches the schema.

        :param content: The content to validate.
        :param schema: The schema to validate against.
        :return: Result true/false with reason.
        """
        self.logger.debug(f"Validating content against schema: {schema}")

        if not isinstance(schema, type):
            self.status = False
            self.reason = "Provided schema is not a class"
            return self.result

        if not issubclass(schema, BaseModel):
            self.status = False
            self.reason = "Provided schema is not a Pydantic model"
            return self.result

        try:
            schema(**content)
            self.status = True
            self.reason = "Content matches schema"
        except ValidationError as e:
            self.status = False
            self.reason = f"Content does not match schema {e}"
        except Exception as e:
            self.status = False
            self.reason = f"Unexpected error occurred during validation: {e}"

        return self.result

