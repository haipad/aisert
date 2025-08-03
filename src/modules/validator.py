from collections import defaultdict
import logging


class BaseValidator:
    """Base class for other validators."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.status = False
        self.reason = ""

    def validate(self) -> dict:
        """Validate content against a schema."""
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def result(self):
        """Return the validation result."""
        return {"status": self.status, "reason": self.reason}
