from enum import Enum


class ValidatorEnums(Enum):
    """
    Enum class for validator types.
    """
    SCHEMA = "SchemaValidator"
    CONTAINS = "ContainsValidator"
    TOKENS = "TokenValidator"
    SEMANTIC = "SemanticValidator"

    @staticmethod
    @property
    def members():
        """
        Returns a list of all validator types.
        """
        return [member.value for member in ValidatorEnums]
