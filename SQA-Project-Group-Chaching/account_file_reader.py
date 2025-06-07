"""
account_file_reader.py

This module handles reading bank account data from a file and converting it into
usable data structures for backend processing. It reads the master bank account file
and validates its format, ensuring that all account details conform to project constraints.

Input:
- A formatted text file containing bank account records.
Output:
- A list of valid bank account dictionaries.
- Error messages for invalid lines in the file.
Usage:
- This module is designed to be used as part of the back-end batch processor.
- It processes the master bank account file to retrieve account details for further processing.
"""
from bank_account import BankAccount

class account_file_reader:

    def __init__(self, file_path: str):
        """
        Initializes the account file reader with the given file path.
        Parameters:
        - file_path (str): The path to the file containing bank account data.
        """
        self.file_path = file_path

    def read_accounts(self) -> list[dict]:
        accounts = []
        with open(self.file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.rstrip('\n')

                # Validate line length (now 45 chars to include plan type)
                if len(clean_line) != 45:
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars, expected 45)")
                    continue

                try:
                    account_number = clean_line[0:4]
                    name = clean_line[6:25]
                    status = clean_line[27]
                    balance_str = clean_line[29:37]
                    transactions_str = clean_line[38:42]
                    plan_type = clean_line[43:45]

                    if not account_number.isdigit():
                        print(f"ERROR: Fatal error - Line {line_num}: Account number must be 5 digits")
                        continue

                    if status not in ('A', 'D'):
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid status '{status}'. Must be 'A' or 'D'")
                        continue

                    if balance_str[0] == '-':
                        print(f"ERROR: Fatal error - Line {line_num}: Negative balance detected: {balance_str}")
                        continue

                    if (len(balance_str) != 8 or 
                        balance_str[5] != '.' or 
                        not balance_str[:5].isdigit() or 
                        not balance_str[6:].isdigit()):
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid balance format. Expected XXXXX.XX, got {balance_str}")
                        continue

                    if not transactions_str.isdigit():
                        print(f"ERROR: Fatal error - Line {line_num}: Transaction count must be 4 digits")
                        continue

                    if plan_type not in ('SP', 'NP'):
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid plan type '{plan_type}'. Must be SP or NP")
                        continue

                    balance = float(balance_str)
                    transactions = int(transactions_str)

                    if balance < 0:
                        print(f"ERROR: Fatal error - Line {line_num}: Negative balance detected")
                        continue
                    if transactions < 0:
                        print(f"ERROR: Fatal error - Line {line_num}: Negative transaction not allowed")
                        continue

                    accounts.append({
                        'account_number': account_number.lstrip('0') or '0',
                        'name': name.strip(),
                        'status': status,
                        'balance': balance,
                        'total_transactions': transactions,
                        'plan': plan_type
                    })

                except Exception as e:
                    print(f"ERROR: Fatal error - Line {line_num}: Unexpected error - {str(e)}")
                    continue

        return accounts

    def convert(self, account_dict: dict) -> BankAccount:
        return BankAccount(
            accountNumber=account_dict['account_number'],
            accountName=account_dict['name'],
            status=account_dict['status'],
            balance=account_dict['balance'],
            totalTransactions=account_dict['total_transactions'],
            plan=account_dict['plan']
    )
