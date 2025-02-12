import hashlib
from decimal import Decimal, InvalidOperation

class BankAccount:
    def __init__(self, account_number, holder_name, password, balance=Decimal("0.00")):
        self.account_number = account_number
        self.holder_name = holder_name
        self.__password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.balance = balance
    
    def authenticate(self, password):
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def deposit(self, amount):
        try:
            amount = Decimal(amount)
            if amount > 0:
                self.balance += amount
                print(f"Deposit successful. New balance: {self.balance}")
            else:
                print("Invalid deposit amount.")
        except InvalidOperation:
            print("Invalid input. Please enter a numeric value.")
    
    def withdraw(self, amount, password):
        if not self.authenticate(password):
            print("Authentication failed. Incorrect password.")
            return
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                print("Invalid withdrawal amount. Must be greater than zero.")
                return
            if amount <= self.balance:
                self.balance -= amount
                print(f"Withdrawal successful. New balance: {self.balance}")
            else:
                print("Invalid withdrawal amount or insufficient funds.")
        except InvalidOperation:
            print("Invalid input. Please enter a numeric value.")
    
    def get_balance(self, password):
        if self.authenticate(password):
            return f"Account Balance: {self.balance}"
        else:
            return "Authentication failed. Incorrect password."


class BankSystem:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, account_number, holder_name, password):
        if account_number in self.accounts:
            print("Account number already exists.")
        else:
            self.accounts[account_number] = BankAccount(account_number, holder_name, password)
            print(f"Account created successfully for {holder_name}.")
    
    def get_account(self, account_number):
        return self.accounts.get(account_number, None)
    

def main():
    bank = BankSystem()
    
    while True:
        print("\nBanking System")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            acc_num = input("Enter Account Number: ")
            name = input("Enter Account Holder Name: ")
            pwd = input("Set Account Password: ")
            bank.create_account(acc_num, name, pwd)
        
        elif choice == "2":
            acc_num = input("Enter Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                amount = input("Enter deposit amount: ")
                account.deposit(amount)
            else:
                print("Account not found.")
        
        elif choice == "3":
            acc_num = input("Enter Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                amount = input("Enter withdrawal amount: ")
                pwd = input("Enter password: ")
                account.withdraw(amount, pwd)
            else:
                print("Account not found.")
        
        elif choice == "4":
            acc_num = input("Enter Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                pwd = input("Enter password: ")
                print(account.get_balance(pwd))
            else:
                print("Account not found.")
        
        elif choice == "5":
            print("Exiting banking system.")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
