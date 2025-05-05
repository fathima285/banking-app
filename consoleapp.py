

accounts={}
#testing git hub=================================
#New Test
def create_account():
    Account_number=int(input("Enter new account number:"))
    while Account_number in accounts:
       print("Account number already exists!")
       return
    Account_holder_name=input("Enter account holder name:")
    try:
        balance=float(input("Enter initial balance:"))
        if balance<0:
            print("Initial balance must be non negative.")
            return
    except ValueError:
        print("invalid input.please enter a number.")
        return
    Accounts[Account_number]={"name":name,"balance":balance,"transactions":[f"Initial_deposit:{balance}"]}
    print("account created successfully.")

    def deposit_money():
        Account_number=input("Enter account number:")
        if Account_number not in accounts:
            print("Account not found.")
            return
        try:
            amount=float(input("Enter amount to deposit:"))
            if amount<=0:
                print("Deposit amount must be positive.")
                return
        except ValueError:
            print("Invalid input.please enter a number.")
            return
        accounts[Account_number]["balance"]+=amount
        accounts[Account_number]["transactions"].append(f"deposited:{amount}")
        print(deposit successfull.)
    def  withdraw_money():
        Account_number=int(input("Enter account number to withdraw from:"))
        if Account_number not in accounts:
            print("Error. account doesn't exist:")
            return
        try:
            amount=float(input("Enter amount to withdraw:"))






