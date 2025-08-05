from collections import defaultdict
import logging

from src.models.result import Result


class BaseValidator:
    """Base class for other validators."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validator_name = name
        self.status = False
        self.reason = ""

    def validate(self) -> dict:
        """Validate content against a schema."""
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def result(self):
        """Return the validation result."""
        return Result(self.status, self.reason)
    
    @property
    def name(self):
        """Return the name of the validator."""
        return self.validator_name
