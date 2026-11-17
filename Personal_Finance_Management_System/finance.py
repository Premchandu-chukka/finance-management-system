from datetime import datetime
from pathlib import Path

class PersonalFinanceManager:
    def __init__(self):
        self.file_name = Path(__file__).with_name("transactions.txt")
        self.transactions = []
        self.monthly_budgets = {}
        self.load_transactions()

    def load_transactions(self):
        if not self.file_name.exists():
            self.file_name.touch()
            return
        with open(self.file_name, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    self.transactions.append({
                        "type": parts[0],
                        "amount": float(parts[1]),
                        "category": parts[2],
                        "date": parts[3],
                        "description": parts[4]
                    })

    def save_transaction(self, item):
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(
                f"{item['type']}|{item['amount']}|{item['category']}|"
                f"{item['date']}|{item['description']}\n"
            )

    def add_transaction(self, kind):
        print(f"\n--- Add {kind} ---")
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
            category = input("Enter category: ").strip()
            if not category:
                print("Category cannot be empty.")
                return
            date_text = input("Enter date (YYYY-MM-DD): ").strip()
            datetime.strptime(date_text, "%Y-%m-%d")
            description = input("Enter description: ").strip().replace("|", "/")
            item = {"type": kind, "amount": amount, "category": category,
                    "date": date_text, "description": description}
            self.transactions.append(item)
            self.save_transaction(item)
            print(f"{kind} added successfully.")
            if kind == "Expense":
                self.check_budget(date_text[:7])
        except ValueError:
            print("Invalid amount or date. Please try again.")

    def get_month_expenses(self, month):
        return sum(x["amount"] for x in self.transactions
                   if x["type"] == "Expense" and x["date"].startswith(month))

    def set_monthly_budget(self):
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
            amount = float(input("Enter monthly budget: "))
            if amount <= 0:
                print("Budget must be greater than zero.")
                return
            self.monthly_budgets[month] = amount
            print("Monthly budget saved for this session.")
            self.check_budget(month)
        except ValueError:
            print("Invalid month or budget.")

    def check_budget(self, month):
        if month in self.monthly_budgets:
            budget = self.monthly_budgets[month]
            spent = self.get_month_expenses(month)
            print(f"Budget: {budget:.2f} | Expenses: {spent:.2f}")
            if spent > budget:
                print("Warning: Monthly budget exceeded.")
            else:
                print(f"Remaining budget: {budget - spent:.2f}")

    def view_transaction_history(self):
        print("\n--- Transaction History ---")
        if not self.transactions:
            print("No transactions found.")
            return
        for x in self.transactions:
            print(f"{x['date']} | {x['type']} | {x['category']} | "
                  f"{x['amount']:.2f} | {x['description']}")

    def category_wise_summary(self):
        totals = {}
        for x in self.transactions:
            if x["type"] == "Expense":
                totals[x["category"]] = totals.get(x["category"], 0) + x["amount"]
        print("\n--- Category-Wise Expense Summary ---")
        if not totals:
            print("No expenses found.")
        for category, amount in totals.items():
            print(f"{category}: {amount:.2f}")

    def calculate_savings(self):
        income = sum(x["amount"] for x in self.transactions if x["type"] == "Income")
        expenses = sum(x["amount"] for x in self.transactions if x["type"] == "Expense")
        print(f"Total Income: {income:.2f}")
        print(f"Total Expenses: {expenses:.2f}")
        print(f"Savings: {income - expenses:.2f}")

    def highest_expense(self):
        expenses = [x for x in self.transactions if x["type"] == "Expense"]
        print("\n--- Highest Expense ---")
        if not expenses:
            print("No expenses found.")
            return
        item = max(expenses, key=lambda x: x["amount"])
        print(f"Category: {item['category']}")
        print(f"Amount: {item['amount']:.2f}")
        print(f"Date: {item['date']}")
        print(f"Description: {item['description']}")

    def monthly_summary(self):
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Use the YYYY-MM date format.")
            return
        income = sum(x["amount"] for x in self.transactions
                     if x["type"] == "Income" and x["date"].startswith(month))
        expenses = self.get_month_expenses(month)
        print(f"\nMonthly Summary: {month}")
        print(f"Income: {income:.2f}")
        print(f"Expenses: {expenses:.2f}")
        print(f"Savings: {income - expenses:.2f}")
        if month in self.monthly_budgets:
            print(f"Budget: {self.monthly_budgets[month]:.2f}")
            print(f"Budget remaining: {self.monthly_budgets[month] - expenses:.2f}")
        else:
            print("No budget set for this month.")
