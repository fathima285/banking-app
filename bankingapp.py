import os

def get_customers_info():
    name=input("Enter Name:")
    adress=input("Enter Adress:")
    username=input("Enter Username:")
    password=input("Enter Password:")

    return[name,address,username,password]

def create_account():
    customers=get_customers_info()
    with open("customers.txt","a") as file:
        file.write(f"{customers[0]},{customers[1]}\n")

def create_user():
    customers=get_customers_info()
    with open ("users.txt","a") as file:
        file.write(f"{customers[2]},{customers[3]}\n")

def create_auto_user():
    with open ("users.txt","r") as user_file:
        user_id=user_file.readlines()[-1].split(",")[0]
        characters=list(user_id)
        