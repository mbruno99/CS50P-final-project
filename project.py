import csv
import difflib

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
            get_transaction("income")

        elif comand_input == "expense":
            get_transaction("expense")

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


def get_transaction(transaction_type):
    """Registra un'entrata o una spesa nel report."""

    if transaction_type == "income":
        categories = income_type
        trans_dict = report["incomes"]
    else:
        categories = expense_type
        trans_dict = report["expenses"]

    while True:
        user_input = input(f"Type of {transaction_type}: ").lower()
        if user_input in categories:
            if user_input not in trans_dict:
                trans_dict[user_input] = get_amount()
                break

            elif user_input in trans_dict:
                while True:
                    choice = input("This amount will be (A)dded or (S)ubtracted from the existing value. select A or S to continue. ").lower().strip()
                    if choice == "a":
                        trans_dict[user_input] += adjust("a")
                        break
                    elif choice == "s":
                        amount = adjust("s")
                        if trans_dict[user_input] - amount < 0:
                            print("Error: The remaining amount cannot be negative.")
                            break
                        else:
                            trans_dict[user_input] -= amount
                            break
                    else:
                        print("choice must be beetween (A)dd or (S)ubtract")
                        continue

            break # per tornare al menu principale
        
        else:
            # Cerchiamo la parola più vicina indicata dall'utente (user_input) nella lista categories, n=1 (prendiamo solo il suggerimento migliore)
            suggestion = difflib.get_close_matches(user_input, categories, n=1)
            # Se suggestion soddisfa la condizione booleana, (se ha trovato una parola simile)
            if suggestion:
                # Stampiamo il primo e unico elemento della lista suggestion
                print(f"Did you mean '{suggestion[0]}'?")
            else:
                print(f"{transaction_type.capitalize()} must be one of the following categories: {', '.join(categories[:-1])} or {categories[-1]}")



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


def adjust(operation):
    while True:
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("The amount must be greater than 0.")
                continue
            return amount  # Restituisce il valore positivo sempre
            
        except ValueError:
            print("The amount must be a number.")



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
