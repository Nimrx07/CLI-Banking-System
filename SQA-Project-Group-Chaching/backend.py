import sys
from bank_database import BankDatabase
from account_file_reader import account_file_reader
from account_file_writer import account_file_writer
from bank_account import BankAccount

def process_transaction(transaction_line, db: BankDatabase):
    parts = transaction_line.strip().split("_")
    code = parts[0]
    name = parts[1].strip()
    acc_num = parts[2]
    amount = float(parts[3])
    misc = parts[4].strip()

    if code == "01":  # Create account
        new_account = BankAccount(acc_num, name, amount, adminPriv=False, status="A", plan=misc)
        db.add_account(new_account)
    elif code == "02":  # Delete account
        db.delete_account(acc_num)
    elif code == "03":  # Deposit
        account = db.get_account(acc_num)
        if account: account.balance += amount
    elif code == "04":  # Withdraw
        account = db.get_account(acc_num)
        if account: account.balance -= amount
    elif code == "05":  # Transfer
        # Not implemented here
        pass
    elif code == "06":  # Paybill
        account = db.get_account(acc_num)
        if account: account.balance -= amount

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python backend.py <current_accounts> <merged_transactions> <master_accounts> <new_current_accounts>")
        sys.exit(1)

    current_file, transactions_file, master_file, new_current_file = sys.argv[1:]

    db = BankDatabase()
    reader = account_file_reader(current_file)
    accounts = reader.read_accounts()
    for acc in accounts:
        db.add_account(acc)

    with open(transactions_file, "r") as tf:
        for line in tf:
            if not line.startswith("00"):  # Skip end-of-session lines
                process_transaction(line, db)

    # Convert BankAccount objects to dictionaries for the writer
    account_dicts = []
    for acc in db.accounts:
        account_dicts.append({
            "account_number": acc.accountNumber,
            "name": acc.accountName,
            "status": acc.status,
            "balance": acc.balance,
            "plan": acc.plan
        })

    # Write using the expected format
    writer_master = account_file_writer(master_file)
    writer_current = account_file_writer(new_current_file)
    writer_master.write_accounts(account_dicts)
    writer_current.write_accounts(account_dicts)
