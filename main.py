import sqlite3
import re
from datetime import datetime
import tabulate

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()


def create_tables():
    sql_statements = [""" CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            date DATE NOT NULL,
            amount FLOAT NOT NULL 
    ); """,
                      """ CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            date DATE NOT NULL,
            amount FLOAT NOT NULL
    ); """]
    try:
        for statement in sql_statements:
            cursor.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        print("Error", e)


def user_selection():
    while True:
        try:
            num = int(input(
                "These are the following options:\n1. Add Income\n2. Add Expense\n3. View Income\n4. View Expenses\n5. Exit application\nEnter a number between 1 and 5: "))
            if 1 <= num <= 5:
                print(f"You entered option: {num}")
                return num
            else:
                print("The number must be between 1 and 5.")
        except ValueError:
            print("Please enter a valid integer.")


def view_income():
    cursor.execute("SELECT * FROM income")
    data = cursor.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Source", "Date", "Amount"], tablefmt="grid"))


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    print(tabulate.tabulate(data, headers=["ID", "Category", "Date", "Amount"], tablefmt="grid"))


def add_income():
    source = input("Where did you get this income from?")
    date = validate_date()
    while True:
        try:
            amount = get_valid_amount("How much did you get? ")
            break
        except ValueError:
            print("Please enter a valid number.")
    sql = """INSERT INTO income(source,date,amount) 
            VALUES(?,?,?)"""
    cursor.execute(sql, (source, date, amount))
    conn.commit()


def add_expenses():
    category = input("What category of item have you spent on e.g. Food or Water Bills?")
    date = validate_date()
    while True:
        try:
            amount = get_valid_amount("How much did you spend? ")
            break
        except ValueError:
            print("Please enter a valid number.")
    sql = """INSERT INTO expenses(category,date,amount) 
            VALUES(?,?,?)"""
    cursor.execute(sql, (category, date, amount))
    conn.commit()


def validate_date():
    while True:
        date_input = input("Enter date in DD-MM-YYYY format: ")
        if re.match(r'^\d{2}-\d{2}-\d{4}$', date_input):
            try:
                valid_date = datetime.strptime(date_input, "%d-%m-%Y").date()
                return valid_date
            except ValueError:
                print("Invalid date. Please enter a valid calendar date.")
        else:
            print("Invalid format. Please enter date in DD-MM-YYYY format.")

def get_valid_amount(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


if __name__ == '__main__':
    create_tables()
    start = False
    while not start:
        choice = user_selection()
        if choice == 5:
            start = True
        elif choice == 1:
            add_income()
        elif choice == 2:
            add_expenses()
        elif choice == 3:
            view_income()
        else:
            view_expenses()
