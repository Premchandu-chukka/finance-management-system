from finance import PersonalFinanceManager

def show_menu():
    print("\n===== PERSONAL FINANCE MANAGEMENT SYSTEM =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Set Monthly Budget")
    print("4. View Transaction History")
    print("5. Category-Wise Expense Summary")
    print("6. Calculate Savings")
    print("7. Identify Highest Expense")
    print("8. Monthly Financial Summary")
    print("9. Exit")

def main():
    finance = PersonalFinanceManager()
    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ").strip()
        if choice == "1":
            finance.add_transaction("Income")
        elif choice == "2":
            finance.add_transaction("Expense")
        elif choice == "3":
            finance.set_monthly_budget()
        elif choice == "4":
            finance.view_transaction_history()
        elif choice == "5":
            finance.category_wise_summary()
        elif choice == "6":
            finance.calculate_savings()
        elif choice == "7":
            finance.highest_expense()
        elif choice == "8":
            finance.monthly_summary()
        elif choice == "9":
            print("Thank you for using the application!")
            break
        else:
            print("Invalid choice. Please enter 1 to 9.")

if __name__ == "__main__":
    main()
