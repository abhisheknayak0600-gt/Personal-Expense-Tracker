
# expenses = []

# def add_expense():
#     category = input("Enter expense category: ")
#     amount = float(input("Enter amount: "))
#     date = input("Enter date (DD-MM-YYYY): ")

#     expense = {
#         "category": category,
#         "amount": amount,
#         "date": date
#     }

#     expenses.append(expense)
#     print("\nExpense added successfully!")


# def view_expenses():
#     if len(expenses) == 0:
#         print("\nNo expenses found!")
#     else:
#         print("\n===== ALL EXPENSES =====")

#         for i, expense in enumerate(expenses, start=1):
#             print(f"{i}. {expense['category']} | Rs. {expense['amount']} | {expense['date']}")


# def total_expenses():
#     total = 0

#     for expense in expenses:
#         total += expense["amount"]

#     print("\nTotal Expenses: Rs.", total)


# def search_expense():
#     category = input("Enter category to search: ").lower()
#     found = False

#     for expense in expenses:
#         if expense["category"].lower() == category:
#             print(expense)
#             found = True

#     if not found:
#         print("No matching expense found!")


# def delete_expense():
#     view_expenses()

#     if len(expenses) > 0:
#         try:
#             choice = int(input("Enter expense number to delete: "))

#             if 1 <= choice <= len(expenses):
#                 removed = expenses.pop(choice - 1)
#                 print("Deleted:", removed)
#             else:
#                 print("Invalid expense number!")

#         except ValueError:
#             print("Please enter a valid number!")


# while True:
#     print("\n===== PERSONAL EXPENSE TRACKER =====")
#     print("1. Add Expense")
#     print("2. View Expenses")
#     print("3. Total Expenses")
#     print("4. Search Expense")
#     print("5. Delete Expense")
#     print("6. Exit")

#     choice = input("Enter your choice: ")

#     if choice == "1":
#         add_expense()

#     elif choice == "2":
#         view_expenses()

#     elif choice == "3":
#         total_expenses()

#     elif choice == "4":
#         search_expense()

#     elif choice == "5":
#         delete_expense()

#     elif choice == "6":
#         print("Thank you for using Expense Tracker!")
#         break

#     else:
#         print("Invalid choice! Try again.")



import sqlite3

# Connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
)
""")

conn.commit()


# Add Expense
def add_expense():
    category = input("Enter category: ")

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Invalid amount!")
        return

    date = input("Enter date (DD-MM-YYYY): ")

    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
        (category, amount, date)
    )

    conn.commit()
    print("Expense added successfully!")


# View Expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()

    if not records:
        print("No expenses found!")
        return

    print("\n===== ALL EXPENSES =====")

    for record in records:
        print(
            "ID:", record[0],
            "| Category:", record[1],
            "| Amount:", record[2],
            "| Date:", record[3]
        )


# Total Expenses
def total_expenses():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()[0]

    total = result if result is not None else 0

    print("Total Expenses: Rs.", total)


# Search Expense
def search_expense():
    category = input("Enter category: ")

    cursor.execute(
        "SELECT * FROM expenses WHERE category LIKE ?",
        ('%' + category + '%',)
    )

    records = cursor.fetchall()

    if records:
        for record in records:
            print(record)
    else:
        print("No matching expense found!")


# Delete Expense
def delete_expense():
    view_expenses()

    try:
        expense_id = int(input("Enter expense ID to delete: "))

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Expense deleted successfully!")
        else:
            print("Expense ID not found!")

    except ValueError:
        print("Invalid ID!")


# Main Menu
while True:

    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expenses")
    print("4. Search Expense")
    print("5. Delete Expense")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        total_expenses()

    elif choice == "4":
        search_expense()

    elif choice == "5":
        delete_expense()

    elif choice == "6":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice!")

conn.close()
