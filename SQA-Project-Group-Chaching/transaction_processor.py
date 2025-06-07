import random
from transaction_dm import Transaction
from session import Session

class TransactionProcessor:
      def deposit(self, session: Session, accounts: list, accountNumber: str, transactionAmnt: float) -> bool:
            account = self.getAccount(accounts, accountNumber)
            if account: 
                  account.balance += transactionAmnt
                  session.addTransaction(Transaction("deposit", accountNumber, transactionAmnt, status = "pending"))
                  return True
            return False
      
      def withdraw(self, session: Session, accounts: list, accountNumber: str, transactionAmnt: float) -> bool:
            """Withdraw money from an account."""
            account = self.getAccount(accounts, accountNumber)
            if session.adminPriv == False and transactionAmnt > 500:
                  return False  # Withdrawal limit for standard users
            if account and (account.balance - transactionAmnt) >= 0:
                  account.balance -= transactionAmnt
                  session.addTransaction(Transaction("withdrawal", accountNumber, transactionAmnt))
                  return True
            return False

      def transfer(self, session: Session, accounts: list, fromAcc: str, toAcc: str, amount: float) -> bool:
            """Transfer money between two accounts."""
            sender = self.getAccount(accounts, fromAcc)
            receiver = self.getAccount(accounts, toAcc)
            if sender and receiver and amount <= 1000 and sender.balance >= amount:
                  sender.balance -= amount
                  receiver.balance += amount
                  session.addTransaction(Transaction("transfer", fromAcc, amount, toAcc))
                  return True
            return False
def create():
        print("please enter the name of the account")
        name = input()
        if len(name) > 20:
            print("the name you entered is too long (the max is 20 charaters)")
        else:
            name_number = str(random.randrange(1,99999))
            with open('accounts.txt') as file:
                contents = file.read()
                search_word = name_number
                if search_word in contents:
                    name_number = random.randrange(1,99999)
            print('your account number is: ' + name_number)
            print("how much money do you want to deposit with cents")
            amount = input()
            if float(amount) > 99999.99:
                print(amount + 'is larger the the max for creating a new acount ($99999.99)')
            file = open("accounts.txt", "a")
            file.write(name)
            file.write(': ')
            file.write(name_number)
            file.write(" $")
            file.write(amount)
            file.close()

def changePlan():
        print('please enter the name of the account you want to change the plan of')
        with open('accounts.txt') as file:
                contents = file.read()
                search_word = input()
                if search_word in contents:
                    print('enter the account number')
                    number = input()
                    with open('acounts.txt') as file:
                        contents = file.read()
                        search_word = number
                        if int(search_word) in contents:
                            print('would you like to change this student account to a non-student account')
                            decision = input()
                            if decision == 'yes':
                                print('the account is now a non-student')
                        else:
                            print('number given is not asscoiated with the name')
                else:
                    print('name not found in system')


def getAccount(self, accounts: list, accountNumber: str):
            """Finds an account by account number."""
            for acc in accounts:
                  if acc.accountNumber == accountNumber:
                        return acc
            return None
