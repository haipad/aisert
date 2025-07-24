import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)
class SchemaValidator:
    """
    A class to validate content against a schema.
    """

    @staticmethod
    def is_schema_match(content: dict, schema):
        """
        Validates if the content matches the schema.
        
        :param content: The content to validate.
        :param schema: The schema to validate against.
        :return: True if content matches schema, False otherwise.
        """
        logger.debug(f"Validating content against schema: {schema}")


        try:
            if not issubclass(schema, BaseModel):
                logger.error("Provided schema is not a Pydantic model")
                return False
        except TypeError:
            logger.error("Provided schema is not a class", exc_info=True)
            return False

        try:
            schema(**content)
        except Exception:
            logger.error("Content does not match schema", exc_info=True)
            return False
       
        return True
