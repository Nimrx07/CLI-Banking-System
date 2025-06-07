"""
account_file_writer.py

This module handles writing bank account data to a file after processing.
It ensures strict adherence to the specified format of the bank system files.

Input:
- A list of bank account dictionaries containing account details.
Output:
- A formatted bank account file adhering to system constraints.
Usage:
- Used in the back-end batch processor to generate updated account files.
- Ensures all written data follows business rules and format constraints.
"""
from bank_account import BankAccount

class account_file_writer:
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_accounts(self, accounts: list[dict]) -> None:
        with open(self.file_path, 'w') as file:
            for acc in accounts:
                # Validate account number
                if not isinstance(acc['account_number'], str) or not acc['account_number'].isdigit():
                    raise ValueError(f"Account number must be numeric string, got {acc['account_number']}")
                if len(acc['account_number']) > 5:
                    raise ValueError(f"Account number exceeds 5 digits: {acc['account_number']}")

                # Validate name
                if len(acc['name']) > 20:
                    raise ValueError(f"Account name exceeds 20 characters: {acc['name']}")

                # Validate status
                if acc['status'] not in ('A', 'D'):
                    raise ValueError(f"Invalid status '{acc['status']}'. Must be 'A' or 'D'")

                # Validate balance with explicit negative check
                if not isinstance(acc['balance'], (int, float)):
                    raise ValueError(f"Balance must be numeric, got {type(acc['balance'])}")
                if acc['balance'] < 0:
                    raise ValueError(f"Negative balance detected: {acc['balance']}")
                if acc['balance'] > 99999.99:
                    raise ValueError(f"Balance exceeds maximum $99999.99: {acc['balance']}")

                # Validate plan type
                plan = acc.get('plan', 'NP')
                if plan not in ('SP', 'NP'):
                    raise ValueError(f"Invalid plan type '{plan}'. Must be SP or NP")

                # Format fields
                acc_num = acc['account_number'].zfill(5)
                name = acc['name'].ljust(20)[:20]
                balance = f"{acc['balance']:08.2f}"

                file.write(f"{acc_num} {name} {acc['status']} {balance} {plan}\n")

            # Add END_OF_FILE marker
            file.write("00000 END_OF_FILE          A 00000.00 NP\n")


    def convert(self, BankAccount: BankAccount) -> dict:
        return {
            'account_number': str(BankAccount.accountNumber),
            'name': BankAccount.accountName,
            'status': BankAccount.status,
            'balance': BankAccount.balance,
            'total_transactions': BankAccount.totalTransactions,
            'plan': BankAccount.plan
        }

