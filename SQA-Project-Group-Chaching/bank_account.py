class BankAccount:
    def __init__(self, accountNumber: int, accountName: str, balance: float, adminPriv: bool = False, status: str = 'A', plan: str = "NP"):
        self.accountNumber = accountNumber
        self.accountName = accountName
        self.adminPriv = adminPriv
        self.balance = balance
        self.status = status  # 'A' for active, 'D' for disabled
        self.plan = plan # 'SP' for student, 'NP' for non-student
        self.transactions = []  # List to store transaction history

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __str__(self):
        return f"Account({self.accountNumber}, {self.accountName}, Balance: {self.balance}, Admin Privileges: {self.adminPriv}, Status: {self.status}, Plan: {self.plan})"
        