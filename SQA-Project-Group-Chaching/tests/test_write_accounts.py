
import tempfile
import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from account_file_writer import account_file_writer

def write_and_read_output(accounts):
    with tempfile.NamedTemporaryFile(delete=False, mode='r+', suffix='.txt') as tmp:
        path = tmp.name
    writer = account_file_writer(path)
    writer.write_accounts(accounts)
    with open(path, 'r') as f:
        result = f.read()
    os.remove(path)
    return result

def test_valid_account_written():
    accounts = [{
        'account_number': '12345',
        'name': 'John Doe',
        'status': 'A',
        'balance': 1234.56,
        'plan': 'SP'
    }]
    output = write_and_read_output(accounts)
    assert "12345 John Doe             A 01234.56 SP" in output
    assert "END_OF_FILE" in output

def test_account_number_not_string():
    accounts = [{
        'account_number': 12345,
        'name': 'Jane Doe',
        'status': 'A',
        'balance': 100.00,
        'plan': 'NP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Account number must be numeric string"):
            writer.write_accounts(accounts)

def test_account_number_too_long():
    accounts = [{
        'account_number': '123456',
        'name': 'Jane Doe',
        'status': 'A',
        'balance': 100.00,
        'plan': 'NP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="exceeds 5 digits"):
            writer.write_accounts(accounts)

def test_name_too_long():
    accounts = [{
        'account_number': '12345',
        'name': 'A very long name that is too long',
        'status': 'A',
        'balance': 100.00,
        'plan': 'NP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Account name exceeds 20 characters"):
            writer.write_accounts(accounts)

def test_invalid_status():
    accounts = [{
        'account_number': '12345',
        'name': 'User',
        'status': 'X',
        'balance': 50.00,
        'plan': 'NP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Invalid status"):
            writer.write_accounts(accounts)

def test_balance_not_numeric():
    accounts = [{
        'account_number': '12345',
        'name': 'User',
        'status': 'A',
        'balance': "123.45",
        'plan': 'SP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Balance must be numeric"):
            writer.write_accounts(accounts)

def test_balance_negative():
    accounts = [{
        'account_number': '12345',
        'name': 'User',
        'status': 'A',
        'balance': -10.00,
        'plan': 'SP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Negative balance"):
            writer.write_accounts(accounts)

def test_balance_too_high():
    accounts = [{
        'account_number': '12345',
        'name': 'User',
        'status': 'A',
        'balance': 100000.00,
        'plan': 'SP'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Balance exceeds maximum"):
            writer.write_accounts(accounts)

def test_invalid_plan_type():
    accounts = [{
        'account_number': '12345',
        'name': 'User',
        'status': 'A',
        'balance': 100.00,
        'plan': 'XX'
    }]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Invalid plan type"):
            writer.write_accounts(accounts)

def test_multiple_valid_accounts():
    accounts = [
        {
            'account_number': '10001',
            'name': 'Alice',
            'status': 'A',
            'balance': 500.00,
            'plan': 'SP'
        },
        {
            'account_number': '10002',
            'name': 'Bob',
            'status': 'A',
            'balance': 750.00,
            'plan': 'NP'
        }
    ]
    output = write_and_read_output(accounts)
    assert "10001 Alice               A 00500.00 SP" in output
    assert "10002 Bob                 A 00750.00 NP" in output
    assert "END_OF_FILE" in output

def test_empty_account_list():
    accounts = []
    output = write_and_read_output(accounts)
    assert output.strip() == "00000 END_OF_FILE          A 00000.00 NP"

def test_mixed_valid_and_invalid_accounts():
    accounts = [
        {
            'account_number': '10003',
            'name': 'Valid User',
            'status': 'A',
            'balance': 500.00,
            'plan': 'SP'
        },
        {
            'account_number': '10004',
            'name': 'Invalid Plan',
            'status': 'A',
            'balance': 500.00,
            'plan': 'ZZ'
        }
    ]
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        writer = account_file_writer(tmp.name)
        with pytest.raises(ValueError, match="Invalid plan type"):
            writer.write_accounts(accounts)
