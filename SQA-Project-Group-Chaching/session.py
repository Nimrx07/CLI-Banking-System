import re 
from bank_account import BankAccount
from transaction_dm import Transaction

class Session:
    def __init__(self, adminPriv: bool, currentAccount: BankAccount):
        self.adminPriv = adminPriv  # A boolean that returns true if the account has admin privileges
        self.currentAccount = currentAccount  # Holds a reference to the logged-in BankAccount
        self.transactions = []  # List of transactions in this session
        
    def validate_name(name):
        """Validates a name based on predefined conditions."""
        if len(name) > 20:
            return "Error: Name should be less than 20 characters."
        if re.search(r'\d', name):
            return "Error: Name should not contain numbers."
        if re.search(r'[^a-zA-Z\s]', name):
            return "Error: Name should not contain special characters."
        return True

    def standard_transaction(transaction):
        """Handles transaction validation for standard users."""
        restricted_transactions = ["create", "delete", "disable", "change plan"]
        if transaction.lower() in restricted_transactions:
            return "Error: Privileged transaction denied for standard user."
        return "Transaction approved."

    def admin_transaction(transaction):
        """Handles transaction validation for admin users."""
        allowed_transactions = ["create", "delete", "disable", "change plan"]
        if transaction.lower() in allowed_transactions:
            return "Transaction approved for admin user."
        return "Error: Invalid transaction for admin."

    def display_bank_account(account_name, account_number="000000", status="Active", amount_of_funds=0):
        """Displays account details."""
        print(f"Account Details: {account_number}_{account_name}_{status}_{amount_of_funds}")

    def login(self):
        """Handles user login and session initialization."""
        print("Hello, welcome to the banking system")

        while True:
            session_type = input("Enter session type (standard/admin): ").strip().lower()
            if session_type in ["standard", "admin"]:
                break
            print("Invalid session type. Please select either 'standard' or 'admin'.")

        while True:
            account_name = input("Please provide the account holder's name: ").strip()
            validation_result = self.validate_name(account_name)
            if validation_result is True:
                break
            print(validation_result)

        if session_type == "standard":
            print("Login successful as Standard user.")
            self.adminPriv = False
            self.currentAccount = account_name  # This should ideally be a `BankAccount` object
            self.display_bank_account(account_name)
            
            transaction = input("Give a transaction to input: ").strip()
            print(self.standard_transaction(transaction))

        elif session_type == "admin":
            print("Login successful as Admin user.")
            self.adminPriv = True
            self.currentAccount = None  # Admins do not have personal accounts
            self.display_bank_account(account_name)
            
            transaction = input("Give a transaction to input: ").strip()
            print(self.admin_transaction(transaction))

    def logout(self):
        """Logs out the current user and clears transactions."""
        self.adminPriv = False
        self.currentAccount = None
        self.transactions = []

    def addTransaction(self, transaction: Transaction):
        """Adds a transaction to the session's history."""
        self.transactions.append(transaction)

    def __str__(self):
        return f"Session({self.adminPriv}, Account: {self.currentAccount}, Transactions: {len(self.transactions)})"
