class Transaction:
    def __init__(self, transactionCode: str, accountNumber: int, transactionAmnt: float):
        self.transactionCode = transactionCode 
        self.accountNumber = accountNumber  # References a BankAccount
        self.transactionAmnt = transactionAmnt

    def __str__(self):
        return f"Transaction({self.transactionCode}, Account: {self.accountNumber}, Amount: {self.transactionAmnt})"