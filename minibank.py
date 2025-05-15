import random
import string
import os
from datetime import datetime
import getpass


DATA_FILE = "accounts.txt"
CREDENTIALS_FILE = "credentials.txt"
TRANSACTION_FILE = "transactions.txt"
ADMIN_CREDENTIALS_FILE = "admin_credentials.txt"


accounts = {}



def generate_account_number():
    while True:
        acc_no = str(random.randint(10000, 99999))
        if acc_no not in accounts:
            return acc_no

def load_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            for line in file:
                try:
                    acc_no, name, balance, txn_str = line.strip().split("|")
                    accounts[acc_no] = {
                        "name": name,
                        "balance": float(balance),
                        "transactions": txn_str.split("#") if txn_str else []
                    }
                except ValueError:
                    print("Warning: Skipping a corrupted line in the file.")

def save_to_file():
    with open(DATA_FILE, "w") as file:
        for acc_no, info in accounts.items():
            transactions = "#".join(info['transactions'])
            file.write(f"{acc_no}|{info['name']}|{info['balance']}|{transactions}\n")

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_transaction(acc_no, message):
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{acc_no}: {message}\n")


def generate_admin_credentials():
    if not os.path.exists(ADMIN_CREDENTIALS_FILE):
        username = "admin_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        with open(ADMIN_CREDENTIALS_FILE, "w") as f:
            f.write(f"{username}:{password}")
        print(f"\n--- Admin Credentials Generated ---\nUsername: {username}\nPassword: {password}")
    else:
        with open(ADMIN_CREDENTIALS_FILE, "r") as f:
            username, password = f.read().strip().split(":")
            print(f"\n--- Admin Credentials ---\nUsername: {username}\nPassword: {password}")

def get_admin_credentials():
    if os.path.exists(ADMIN_CREDENTIALS_FILE):
        with open(ADMIN_CREDENTIALS_FILE, "r") as f:
            return f.read().strip().split(":")
    return None, None

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. View All Transactions")
        print("4. Logout")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            create_account()
        elif choice == "2":
            view_all_accounts()
        elif choice == "3":
            view_all_transactions()
        elif choice == "4":
            print("Logging out of admin account.")
            break
        else:
            print("Invalid choice. Please try again.")

def create_account():
    name = input("Enter account holder's name: ").strip()
    try:
        initial_balance = float(input("Enter initial deposit amount: "))
        if initial_balance < 0:
            print("Initial balance cannot be negative.")
            return
    except ValueError:
        print("Please enter a valid numeric amount.")
        return

    acc_no = generate_account_number()

    while True:
        pin = getpass.getpass("Create a 4-digit PIN: ").strip()
        confirm_pin = getpass.getpass("Confirm your PIN: ").strip()
        if pin != confirm_pin:
            print("PINs do not match. Try again.")
        elif not (pin.isdigit() and len(pin) == 4):
            print("PIN must be exactly 4 digits.")
        else:
            break

    accounts[acc_no] = {
        "name": name,
        "balance": initial_balance,
        "transactions": [f"{get_timestamp()} - Account created with balance ${initial_balance:.2f}"]
    }

    with open(CREDENTIALS_FILE, "a") as f:
        f.write(f"{acc_no}:{pin}:user\n")

    log_transaction(acc_no, f"{get_timestamp()} - Account created with balance ${initial_balance:.2f}")
    print(f"Account successfully created! Your Account Number is: {acc_no}")

def view_all_accounts():
    if not accounts:
        print("No accounts to display.")
        return
    print("\n--- List of All Accounts ---")
    for acc_no, info in accounts.items():
        print(f"Account No: {acc_no} | Name: {info['name']} | Balance: ${info['balance']:.2f}")

def Total_transactions(transactions):
    if os.path.exists(TRANSACTION_FILE):
        print("\n--- Total Transactions ---")
        with open(TRANSACTION_FILE, "r") as f:
            for line in f:
                print(line.strip())
    else:
        print("No transactions found.")



def customer_menu(acc_no):
    name = accounts[acc_no]["name"]
    while True:
        print(f"\n--- Welcome, {name}! ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. View Transactions")
        print("5. Logout")

        choice = input("Select an option: ").strip()
        if choice == "1":
            deposit_money(acc_no)
        elif choice == "2":
            withdraw_money(acc_no)
        elif choice == "3":
            check_balance(acc_no)
        elif choice == "4":
            show_transactions(acc_no)
        elif choice == "5":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

def deposit_money(acc_no):
    try:
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Deposit amount cannot be negative and Deposit amount must be positive.")
            return
        accounts[acc_no]["balance"] += amount
        msg = f"{get_timestamp()} - Deposited Rs.{amount:.2f}"
        accounts[acc_no]["transactions"].append(msg)
        log_transaction(acc_no, msg)
        print("Deposit successful.")
    except ValueError:
        print("Invalid input.Please enter a number.")

def withdraw_money(acc_no):
    try:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Withdrawal must be a positive number.")
            return
        if accounts[acc_no]["balance"] >= amount:
            accounts[acc_no]["balance"] -= amount
            msg = f"{get_timestamp()} - Withdrew Rs.{amount:.2f}"
            accounts[acc_no]["transactions"].append(msg)
            log_transaction(acc_no, msg)
            print("Withdrawal successful.")
        else:
            print("Insufficient balance.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def check_balance(acc_no):
    balance = accounts[acc_no]['balance']
    print(f"Your current balance is: Rs{balance:.2f}")

def show_transactions(acc_no):
    print("\n--- Your Transaction History ---")
    for txn in accounts[acc_no]["transactions"]:
        print("   •", txn)

def verify_credentials(acc_no, pin):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            for line in f:
                try:
                    stored_acc, stored_pin, role = line.strip().split(":")
                    if stored_acc == acc_no and stored_pin == pin:
                        return role
                except ValueError:
                    continue
    return None



def main():
    generate_admin_credentials()
    load_from_file()

    MAX_ATTEMPTS=3

    while True:
        print("\n=== Welcome to the Mini Banking App ===")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
           attempts=0
           if attempts<MAX_ATTEMPTS:

            username_input = input("Enter admin username: ").strip()
            password_input = getpass.getpass("Enter admin password: ").strip()
            admin_username, admin_password = get_admin_credentials()

            if username_input == admin_username and password_input == admin_password:
                admin_menu()
            else:
                print("Incorrect admin credentials.")

           elif attempts=+1
                print("invalid input,attempts remaining")

           elif attempts=MAX_ATTEMPTS
                print("Too many attemps.Exiting programme")
                return
                
            
        elif choice == "2":
            acc_no = input("Enter your account number: ").strip()
            pin = getpass.getpass("Enter your 4-digit PIN: ").strip()
            role = verify_credentials(acc_no, pin)
            if role == "user" and acc_no in accounts:
                customer_menu(acc_no)
            else:
                print("Invalid account number or PIN.")
        elif choice == "3":
            save_to_file()
            print("Thank you for using the Mini Banking App. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")


main()