import logging

from ..models.result import Result


class BaseValidator:
    """Base class for other validators."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validator_name = name

    def validate(self, *args, **kwargs) -> dict:
        """Validate content against a schema."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    @property
    def name(self):
        """Return the name of the validator."""
        return self.validator_name