import random
import os
from datetime import datetime


accounts = {}

# -----------------------------
# Helper Functions
# -----------------------------

def generate_account_number():
    """Generate a unique 5-digit account number."""
    while True:
        acc_no = str(random.randint(10000, 99999))
        if acc_no not in accounts:
            return acc_no

def load_from_file(filename="accounts.txt"):
    """Load all account data from a text file into memory."""
    if os.path.exists(filename):
        with open(filename, "r") as file:
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

def save_to_file(filename="accounts.txt"):
    """Save all account data back to the text file."""
    with open(filename, "w") as file:
        for acc_no, info in accounts.items():
            transactions = "#".join(info['transactions'])
            file.write(f"{acc_no}|{info['name']}|{info['balance']}|{transactions}\n")

def get_timestamp():
    """Return the current time formatted as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# Admin Features
# -----------------------------

def admin_menu():
    """Display and handle admin menu operations."""
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
    """Create a new bank account."""
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
    accounts[acc_no] = {
        "name": name,
        "balance": initial_balance,
        "transactions": [f"{get_timestamp()} - Account created with balance {initial_balance}"]
    }

    print(f"Account successfully created! Your Account Number is: {acc_no}")

def view_all_accounts():
    """List all accounts with details."""
    if not accounts:
        print("No accounts to display.")
        return

    print("\n--- List of All Accounts ---")
    for acc_no, info in accounts.items():
        print(f"Account No: {acc_no} | Name: {info['name']} | Balance: ${info['balance']:.2f}")

def view_all_transactions():
    """Display transaction history for all accounts."""
    if not accounts:
        print("No accounts available.")
        return

    print("\n--- Transaction History ---")
    for acc_no, info in accounts.items():
        print(f"\nAccount Number: {acc_no} - {info['name']}")
        for txn in info['transactions']:
            print("   •", txn)

# -----------------------------
# Customer Features
# -----------------------------

def customer_menu(acc_no):
    """Display and handle customer actions."""
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
    """Deposit money into the customer's account."""
    try:
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Deposit must be a positive number.")
            return

        accounts[acc_no]["balance"] += amount
        accounts[acc_no]["transactions"].append(f"{get_timestamp()} - Deposited ${amount:.2f}")
        print("Deposit successful.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def withdraw_money(acc_no):
    """Withdraw money from the customer's account."""
    try:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Withdrawal must be a positive number.")
            return

        if accounts[acc_no]["balance"] >= amount:
            accounts[acc_no]["balance"] -= amount
            accounts[acc_no]["transactions"].append(f"{get_timestamp()} - Withdrew ${amount:.2f}")
            print("Withdrawal successful.")
        else:
            print("Insufficient balance.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def check_balance(acc_no):
    """Show the current balance of the customer's account."""
    balance = accounts[acc_no]['balance']
    print(f"Your current balance is: ${balance:.2f}")

def show_transactions(acc_no):
    """Display transaction history for the customer's account."""
    print("\n--- Your Transaction History ---")
    for txn in accounts[acc_no]["transactions"]:
        print("   •", txn)

# -----------------------------
# Main Program Entry Point
# -----------------------------

def main():
    """Main function to run the banking system."""
    load_from_file()

    while True:
        print("\n=== Welcome to the Mini Banking App ===")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            password = input("Enter admin password: ").strip()
            if password == "admin123":
                admin_menu()
            else:
                print("Incorrect password.")
        elif choice == "2":
            acc_no = input("Enter your account number: ").strip()
            if acc_no in accounts:
                customer_menu(acc_no)
            else:
                print("Account not found.")
        elif choice == "3":
            save_to_file()
            print("Thank you for using the Mini Banking App. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

# Start the program
main()