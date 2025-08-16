class AisertReport:
    """
    Represents the final validation report from Aisert operations.

    Contains the overall validation status and detailed results from each validator
    that was executed during the validation chain.

    Attributes:
        status (bool): Overall validation status. True if all validations passed.
        rules (dict): Dictionary containing detailed results from each validator,
                     keyed by validator name (e.g., 'SchemaValidator', 'ContainsValidator').

    Example:
        >>> result = Aisert(content).assert_contains(['test']).collect()
        >>> print(result.status)  # True/False
        >>> print(result.rules)   # {'ContainsValidator': {'status': True, 'reason': '...'}}
    """

    def __init__(self, status, rules):
        self.status = status
        self.rules = rules

    def __str__(self):
        return f"Status: {self.status} \n Rules: {self.rules}"
