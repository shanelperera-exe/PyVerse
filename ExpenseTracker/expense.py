import datetime

class Expense:
    def __init__(self, amount:float, category:str, description:str):
        assert amount >= 0, f"Amount {amount} is invalid."

        self.date = self.get_date()
        self.amount = amount
        self.category = category
        self.description = description

    @staticmethod
    def get_date():
        return datetime.datetime.now().date().strftime("%Y-%m-%d")
    
    