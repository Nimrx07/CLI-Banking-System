"""
bank_database.py

This module manages the in-memory representation of bank accounts. It provides
functionalities to retrieve, add, and delete bank accounts from the system.
Usage:
- Used as part of the back-end batch processor to store and manage accounts.
- Allows access to account data for processing transactions.

"""
from bank_account import BankAccount

class BankDatabase:
    def __init__(self):
        """
        Initializes an empty internal list/array for storing bank accounts.
        """
        self.accounts = []

    def get_account(self, account_number: str) -> BankAccount:
        """
        Retrieves a BankAccount object based on the given account number.

        Parameters:
        - account_number (str): The account number to search for.
        Returns:
        - BankAccount: The BankAccount object if found, otherwise None.
        """
        for account in self.accounts:
            if str(account.accountNumber) == account_number:
                return account
        return None  # Account not found

    def add_account(self, account: BankAccount) -> None:
        self.accounts.append(account)

    def delete_account(self, account_number: str) -> None:
        self.accounts = [account for account in self.accounts if str(account.accountNumber) != account_number]

    def log_constraint_error(self, description, context, fatal=False):
        if fatal:
            print(f"ERROR: Fatal error - File {context} - {description}")
            #exit system code here
        else:
            print(f"ERROR: {context}: {description}")
