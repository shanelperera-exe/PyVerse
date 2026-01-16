from expense import Expense
import csv

class ExpenseManager:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.expenses : list[Expense] = []
        self.load_expenses()
    
    def load_expenses(self):
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expense = Expense(
                        amount= float(row["amount"]),
                        category=row["category"],
                        description=row["description"]
                    )
                    expense.date = row["date"]
                    self.expenses.append(expense)
        except FileNotFoundError:
            print("")
            self.expenses = []

    def save_expenses(self):
        with open(self.file_path, mode="w", newline="") as file:
            fieldnames = ["date", "amount", "category", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow({
                    "date": expense.date,
                    "amount": {expense.amount},
                    "category": expense.category,
                    "description": expense.description
                })

    def add_expense(self, amount:float, category:str, description:str):
        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self.save_expenses()

    def get_all_expenses(self):
        return self.expenses
    
    def get_total_spent(self) -> float:
        return sum(expense.amount for expense in self.expenses)
    
    def get_category_summary(self) -> dict:
        summary = {}
        for expense in self.expenses:
            summary.setdefault(expense.category, 0)
            summary[expense.category] += expense.amount
        return summary
