from typing import List

from .validator import BaseValidator
from ..exception import ContainsValidationError
from ..models.result import Result


class ContainsValidator(BaseValidator):
    """
    Validates if a text contains a specific substring.
    """

    def __init__(self, invert=False):
        super().__init__("ContainsValidator")
        self.invert = invert

    def validate(self, content, items: List) -> Result:
        """
        Validate if the content contains the specified substring.
        """
        if not isinstance(items, list):
            raise ContainsValidationError("items must be a list")

        # Capture both missing and found in single pass
        missing, found = [], []
        for item in items:
            (found if item in content else missing).append(item)

        if self.invert:
            # For assert_not_contains: success when nothing is found
            success = len(found) == 0
            reason = f"Found flagged items: {found}" if found else "No flagged items found"
        else:
            # For assert_contains: success when nothing is missing
            success = len(missing) == 0
            reason = f"Missing items: {missing}" if missing else f"Found all items: {found}"

        return Result(success, reason)
