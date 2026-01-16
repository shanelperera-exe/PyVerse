from ExpenseManager import ExpenseManager

def main():
    manager = ExpenseManager("expenses.csv")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense_ui(manager)
        elif choice == "2":
            view_all_expenses_ui(manager)
        elif choice == "3":
            view_total_spending_ui(manager)
        elif choice == "4":
            view_category_summary_ui(manager)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def show_menu():
    print("\n*** Personal Expense Tracker ***")
    print("[1] Add expense")
    print("[2] View all expenses")
    print("[3] View total spending")
    print("[4] View spending by category")
    print("[5] Exit")

def add_expense_ui(manager: ExpenseManager):
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()

        manager.add_expense(amount, category, description)
        print("Expense added successfully.")
    except ValueError:
        print("Invalid input. Amount must be a number.")

def view_all_expenses_ui(manager: ExpenseManager):
    expenses = manager.get_all_expenses()

    if not expenses:
        print("No expenses recorded.")
        return
    
    print("\nDate | Amount | Category | Description")
    print("-" * 50)

    for expense in expenses:
        print(
            f"{expense.date} | "
            f"{expense.amount:.2f} | "
            f"{expense.category} | "
            f"{expense.description}"
        )

def view_total_spending_ui(manager: ExpenseManager):
    total = manager.get_total_spent()
    print(f"\nTotal spent: {total:.2f}")


def view_category_summary_ui(manager: ExpenseManager):
    summary = manager.get_category_summary()

    if not summary:
        print("No expenses recorded.")
        return

    print("\nCategory | Total Spent")
    print("-" * 30)

    for category, total in summary.items():
        print(f"{category} | {total:.2f}")


if __name__ == "__main__":
    main()