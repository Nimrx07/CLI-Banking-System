import json
from bank_account import BankAccount

class FileManager:
    def readAccountsFile(self, filePath: str) -> list:
        """Reads bank account data from a file."""
        accounts = []
        with open(filePath, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                accounts.append(BankAccount(data[0], data[1], float(data[2]), data[3]))
        return accounts

    def writeAccountsFile(self, filePath: str, accounts: list):
        """Writes bank accounts to a file."""
        with open(filePath, 'w') as file:
            for acc in accounts:
                file.write(f"{acc.accountNumber},{acc.accountName},{acc.balance},{acc.status}\n")

    def writeTransactionsFile(self, filePath: str, transactions: list):
        """Writes transactions to a file."""
        with open(filePath, 'w') as file:
            for trans in transactions:
                file.write(f"{trans.transactionCode},{trans.accountNumber},{trans.amount},{trans.misc}\n")
