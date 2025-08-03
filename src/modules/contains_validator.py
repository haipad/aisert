from src.modules.validator import BaseValidator


class ContainsValidator(BaseValidator):
    """
    Validates if a text contains a specific substring.
    """

    def __init__(self, substring: str):
        super().__init__()

    def validate(self, content, items: list) -> bool:
        """
        Validate if the content contains the specified substring.
        
        :param content: The content to validate.
        :return: True if the content contains the substring, False otherwise.
        """
        if not isinstance(items, list):
            self.status = False
            self.reason = "Items must be a list and not {}".format(type(items))
        else:
            c = []
            n = []
            for item in items:
                if item in content:
                    c.append(item)
                else:
                    n.append(item)
            self.status = len(n) == 0
            self.reason = f"Not Contains: {n or '[]'}"
        return self.result