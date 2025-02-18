import csv

income_type = ["salary", "extra earnings", "investments", "pensions", "refunds", "gifts"]
expense_type = ["housing","groceries","transportation","healthcare","leisure","debt" ]

report = {
    "incomes": {},
    "expenses": {}
}


def main():
    input("Welcome to Budget Pal! Press Enter to continue.")
    input("What would you like to register? Press Enter to continue.")

    while True:
        comand_input = input("Enter 'income', 'expense', 'report', 'save' or 'exit': ").lower().strip()
        if comand_input == "income":
            get_income()
        elif comand_input == "expense":
            get_expense()
        elif comand_input == "report":
            if not report["incomes"] and not report["expenses"]:
                print("Nothing recorded yet.")
            else:
                print_report()
            break
        elif comand_input == "save":
            save_to_csv()
        elif comand_input == "exit":
            save_to_csv()
            print("Goodbye!")
            break
        else:
            print("Invalid command.")


def get_income():
    while True:
        user_income = input("Type of Income: ").lower()
        if user_income in income_type:
            if user_income in report["incomes"]:
                input("This amount will be added or subtracted from the existing value. Press Enter to continue.")
                report["incomes"][user_income] += adjust()
                break

            elif user_income not in report["incomes"]:
                report["incomes"][user_income] = get_amount()
                break

        else:
            print(f"Income must be one of the following categories: {", ".join(income_type[0:5])} or {income_type[5]}")
            continue


def get_expense():
    while True:
        user_expense = input("Type of Expense: ").lower()
        if user_expense in expense_type:
            if user_expense in report["expenses"]:
                input("This amount will be added or subtracted from the existing value. Press Enter to continue.")
                report["expenses"][user_expense] += adjust()
                break

            elif user_expense not in report["expenses"]:
                report["expenses"][user_expense] = get_amount()
                break

        else:
            print(f"Expense must be one of the following categories: {", ".join(expense_type[0:5])} or {expense_type[5]}")
            continue

def get_sub_keys():
    sub_keys_income = []
    sub_keys_expense = []

    for category in report["incomes"].keys():
        sub_keys_income.append(category)

    for category1 in report["expenses"].keys():
        sub_keys_expense.append(category1)

    return sub_keys_income, sub_keys_expense


def print_report():
    sub_keys_income, sub_keys_expense = get_sub_keys()

    total_income = sum(report["incomes"].values())
    total_expense = sum(report["expenses"].values())

    print("\n===== BUDGET REPORT =====\n")

    for income in sub_keys_income:
        print(f"Incomes ({income}): {report['incomes'].get(income):.2f}")
    print(f"Total income: {total_income:.2f}")

    print()

    for expense in sub_keys_expense:
        print(f"Expenses ({expense}): {report['expenses'].get(expense):.2f}")
    print(f"Total expenses: {total_expense:.2f}")

    print()

    difference = total_income - total_expense
    if difference > 0:
        print(f":) Great job! Net savings: {difference:.2f}")
    elif difference < 0:
        print(f":( Be careful! Net loss: {difference:.2f}")
    else:
        print(f"You broke even! :/")



def get_amount():
    while True:
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("The amount must be greater than 0.")
                continue
            return amount

        except ValueError:
            print("The amount must be a number.")
            continue


def adjust():
    while True:
        try:
            amount = float(input("Amount: "))
            return amount

        except ValueError:
            print("The amount must be a number.")
            continue


def save_to_csv():
    with open("budget.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["type", "category", "amount"])

        # Usiamo .items() per iterare sia sulle sulle chiavi che su i valori del dizionario
        for category, amount in report["incomes"].items():
            writer.writerow(["income", category, amount])

        # Usiamo .items() per iterare sia sulle sulle chiavi che su i valori del dizionario
        for category, amount in report["expenses"].items():
            writer.writerow(["expense", category, amount])

    print("Data saved successfully!")


if __name__ == "__main__":
    main()
