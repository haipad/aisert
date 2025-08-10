

class AisertReport:
    def __init__(self, status, rules):
        self.status = status
        self.rules = rules
    

    def __str__(self):
        return f"Status: {self.status} \n Rules: {self.rules}"