

from typing import Dict

from ..models.validator_enums import ValidatorEnums


class Result:
    """
    Represents the result of a validation operation.
    Contains status and reason for the validation result.
    """

    def __init__(self, status: bool, reason: str = ""):
        """
        Initializes the Result with a status and an optional reason.
        :param status: The status of the validation (True or False).
        :param reason: The reason for the validation result.
        """
        self.status = status
        self.reason = reason
    
    def to_dict(self) -> Dict[str, str]:
        """
        Converts the Result object to a dictionary.
        :return: A dictionary containing the status and reason.
        """
        return {"status": self.status, "reason": self.reason}


class AisertStatus:
    """
    Represents the status of an Aisert operation.
    Contains the status and reason for the operation.
    """

    def __init__(self):
        """
        Initializes the AisertStatus with a validator type, status, and an optional reason.
        :param validator: The type of validator used for the operation.
        :param status: The status of the operation (True or False).
        :param reason: The reason for the operation result.
        """
        self.validators = {validator.value: None for validator in ValidatorEnums}

    def update(self, validator: str, result: Result):
        """
        Updates the status of a specific validator.
        :param validator: The type of validator to update.
        :param status: The status of the validator (True or False).
        :param reason: The reason for the validator's status.
        """
        if validator in ValidatorEnums.members():
            self.validators[validator] = result

    def collect(self) -> Dict[str, Result]:
        """
        Collects the status of all validators.
        :return: A dictionary containing the status of each validator.
        """
        return {k: v for k, v in self.validators.items() if v is not None}
