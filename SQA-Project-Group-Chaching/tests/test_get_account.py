import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bank_database import BankDatabase
from bank_account import BankAccount

def test_get_account_found():
    db = BankDatabase()
    acc = BankAccount("12345", "John Doe", "A", 1000.00, 0, "SP")
    db.add_account(acc)
    assert db.get_account("12345") == acc

def test_get_account_not_found():
    db = BankDatabase()
    acc = BankAccount("54321", "Jane Doe", "A", 500.00, 0, "NP")
    db.add_account(acc)
    assert db.get_account("99999") is None

def test_get_account_empty_database():
    db = BankDatabase()
    assert db.get_account("12345") is None

def test_get_account_empty_string():
    db = BankDatabase()
    acc = BankAccount("123", "Short ID", "A", 100.00, 0, "SP")
    db.add_account(acc)
    assert db.get_account("") is None

def test_get_account_leading_zero_match():
    db = BankDatabase()
    acc = BankAccount("00001", "Leading Zero", "A", 250.00, 0, "NP")
    db.add_account(acc)
    assert db.get_account("00001") == acc
