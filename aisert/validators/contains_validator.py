from typing import List

from .validator import BaseValidator
from ..exception import ContainsValidationError
from ..models.result import Result


class ContainsValidator(BaseValidator):
    """
    Validates if a text contains a specific substring.
    """

    def __init__(self):
        super().__init__("ContainsValidator")

    def validate(self, content, items: List) -> Result:
        """
        Validate if the content contains the specified substring.
        
        :param content: The content to validate.
        :param items: List of items to be checked for
        :return: True if the content contains the substring, False otherwise.
        """
        if not isinstance(items, list):
            raise ContainsValidationError(False, f"items must be a list")
        missing = [item for item in items if item not in content]
        return Result(len(missing) == 0, f"Missing: {missing or '[None]'}")
