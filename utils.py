import csv
from datetime import datetime
from flask import current_app
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file_path, row, fieldnames):
    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(row)

def format_currency(value):
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return f"${0:,.2f}"

def format_date(date):
    return date.strftime("%Y-%m-%d")

def get_accounts():
    try:
        with open(current_app.config['ACCOUNTS_FILE'], 'r') as f:
            reader = csv.DictReader(f)
            accounts = list(reader)
        
        logger.debug(f"Loaded {len(accounts)} accounts from file")
        
        # Ensure each account has a category
        for account in accounts:
            if 'category' not in account or not account['category']:
                account['category'] = get_account_category(account['id'])
            print(f"Account: {account['name']}, Category: {account['category']}")
        
        return accounts
    except FileNotFoundError:
        logger.warning("Accounts file not found")
        return []

def get_account_category(account_id):
    predefined_accounts = get_predefined_accounts()
    for category, subcategories in predefined_accounts.items():
        for subcategory, accounts in subcategories.items():
            for code, name in accounts:
                if code == account_id:
                    return category
    return 'Uncategorized'

def get_account_info(account_id):
    predefined_accounts = get_predefined_accounts()
    for category, subcategories in predefined_accounts.items():
        for subcategory, accounts in subcategories.items():
            for code, name in accounts:
                if code == account_id:
                    return {'category': category, 'subcategory': subcategory}
    return None

def get_journal_entries():
    return read_csv(current_app.config['JOURNAL_ENTRIES_FILE'])

def get_predefined_accounts():
    return {
        'Assets': {
            'Current Assets': [
                ('1000', 'Cash on Hand'),
                ('1010', 'Cash in Bank'),
                ('1020', 'Petty Cash'),
                ('1100', 'Accounts Receivable'),
                ('1200', 'Inventory - Cars'),
                ('1210', 'Inventory - Parts and Accessories'),
                ('1300', 'Prepaid Expenses')
            ],
            'Fixed Assets': [
                ('1500', 'Land'),
                ('1510', 'Buildings'),
                ('1520', 'Leasehold Improvements'),
                ('1530', 'Office Equipment'),
                ('1540', 'Computer Equipment'),
                ('1550', 'Furniture and Fixtures'),
                ('1560', 'Vehicles'),
                ('1570', 'Accumulated Depreciation')
            ]
        },
        'Liabilities': {
            'Current Liabilities': [
                ('2000', 'Accounts Payable'),
                ('2100', 'Short-term Loans'),
                ('2200', 'Sales Tax Payable'),
                ('2300', 'Payroll Liabilities'),
                ('2400', 'Unearned Revenue'),
                ('2500', 'Customer Deposits')
            ],
            'Long-term Liabilities': [
                ('2600', 'Long-term Loans'),
                ('2700', 'Mortgage Payable')
            ]
        },
        'Equity': {
            'Owner\'s Equity': [
                ('3000', 'Owner\'s Capital'),
                ('3010', 'Owner\'s Drawings'),
                ('3100', 'Retained Earnings')
            ]
        },
        'Revenue': {
            'Sales Revenue': [
                ('4000', 'Car Sales Revenue'),
                ('4010', 'Parts and Accessories Sales'),
                ('4020', 'Service Revenue'),
                ('4030', 'Extended Warranty Revenue'),
                ('4040', 'Financing Revenue')
            ],
            'Other Revenue': [
                ('4100', 'Advertising Revenue'),
                ('4200', 'Interest Income')
            ]
        },
        'Cost of Goods Sold': {
            'COGS': [
                ('5000', 'Cost of Cars Sold'),
                ('5010', 'Cost of Parts and Accessories Sold'),
                ('5020', 'Cost of Services')
            ]
        },
        'Operating Expenses': {
            'Selling Expenses': [
                ('6000', 'Advertising and Promotion'),
                ('6010', 'Sales Commissions'),
                ('6020', 'Website Maintenance'),
                ('6030', 'Marketing Expenses')
            ],
            'Administrative Expenses': [
                ('6100', 'Office Supplies'),
                ('6110', 'Rent Expense'),
                ('6120', 'Utilities Expense'),
                ('6130', 'Insurance Expense'),
                ('6140', 'Depreciation Expense'),
                ('6150', 'Salaries and Wages'),
                ('6160', 'Payroll Taxes'),
                ('6170', 'Professional Fees')
            ],
            'Other Operating Expenses': [
                ('6200', 'Vehicle Maintenance'),
                ('6210', 'Fuel and Oil'),
                ('6220', 'Licensing and Registration'),
                ('6230', 'Training and Development'),
                ('6240', 'Bank Charges'),
                ('6250', 'Travel and Entertainment')
            ]
        },
        'Non-Operating Expenses': {
            'Other Expenses': [
                ('7000', 'Interest Expense'),
                ('7100', 'Loss on Sale of Assets')
            ]
        }
    }

def initialize_accounts():
    accounts = get_accounts()
    if not accounts:
        predefined_accounts = get_predefined_accounts()
        for category, subcategories in predefined_accounts.items():
            for subcategory, accounts_list in subcategories.items():
                for account_code, account_name in accounts_list:
                    add_account(account_code, account_name, category, subcategory)

def save_accounts(accounts):
    fieldnames = ['id', 'name', 'category', 'subcategory', 'balance']
    with open(current_app.config['ACCOUNTS_FILE'], 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for account in accounts:
            writer.writerow({
                'id': account['id'],
                'name': account['name'],
                'category': account.get('category', ''),
                'subcategory': account.get('subcategory', ''),
                'balance': account.get('balance', '0.00')
            })

def add_account(account_code, account_name, category, subcategory):
    accounts = get_accounts()
    new_account = {
        'id': account_code,
        'name': account_name,
        'category': category,
        'subcategory': subcategory,
        'balance': '0.00'
    }
    accounts.append(new_account)
    save_accounts(accounts)

def update_account(account_id, updated_account):
    accounts = get_accounts()
    for account in accounts:
        if account['id'] == account_id:
            account.update(updated_account)
            break
    save_accounts(accounts)

def delete_account(account_id):
    accounts = get_accounts()
    accounts = [account for account in accounts if account['id'] != account_id]
    save_accounts(accounts)

def add_journal_entry(date, description, debit_account_id, credit_account_id, amount):
    entries = get_journal_entries()
    new_id = str(max([int(entry['id']) for entry in entries] + [0]) + 1)
    new_entry = {
        'id': new_id,
        'date': date,
        'description': description,
        'debit_account_id': debit_account_id,
        'credit_account_id': credit_account_id,
        'amount': amount
    }
    logger.debug(f"Adding new journal entry: {new_entry}")
    try:
        append_csv(current_app.config['JOURNAL_ENTRIES_FILE'], new_entry, ['id', 'date', 'description', 'debit_account_id', 'credit_account_id', 'amount'])
        logger.info(f"Successfully added journal entry with ID {new_id}")
    except Exception as e:
        logger.error(f"Failed to add journal entry: {str(e)}")
        raise
    return new_entry

def get_journal_entries():
    try:
        with open(current_app.config['JOURNAL_ENTRIES_FILE'], 'r') as f:
            reader = csv.DictReader(f)
            entries = list(reader)
        
        logger.debug(f"Raw CSV contents: {entries}")
        
        for entry in entries:
            # Check for 'amount' or 'amount1' field
            if 'amount' in entry and entry['amount']:
                entry['amount'] = entry['amount']
            elif 'amount1' in entry and entry['amount1']:
                entry['amount'] = entry['amount1']
            else:
                entry['amount'] = '0.00'
                logger.warning(f"Journal entry {entry.get('id', 'unknown')} is missing amount field. Set to 0.00.")
            
            # Remove extra fields
            keys_to_remove = [key for key in entry.keys() if key not in ['id', 'date', 'description', 'debit_account_id', 'credit_account_id', 'amount']]
            for key in keys_to_remove:
                del entry[key]
            
            logger.debug(f"Processed entry: {entry}")
        
        return entries
    except FileNotFoundError:
        logger.warning("Journal entries file not found. Returning empty list.")
        return []

def update_account_balances():
    accounts = get_accounts()
    entries = get_journal_entries()
    
    for account in accounts:
        balance = 0
        for entry in entries:
            if entry['debit_account_id'] == account['id']:
                if account['category'] in ['Assets', 'Expenses']:
                    balance += float(entry['amount'])
                else:
                    balance -= float(entry['amount'])
            if entry['credit_account_id'] == account['id']:
                if account['category'] in ['Assets', 'Expenses']:
                    balance -= float(entry['amount'])
                else:
                    balance += float(entry['amount'])
        account['balance'] = str(balance)
    
    save_accounts(accounts)
# Add more utility functions as needed
def calculate_account_balance(account):
    # Calculate account balance based on transactions
    debit_sum = sum(t.amount for t in account.transactions if t.type == 'debit')
    credit_sum = sum(t.amount for t in account.transactions if t.type == 'credit')
    
    if account.type in ['asset', 'expense']:
        return debit_sum - credit_sum
    else:
        return credit_sum - debit_sum

class DateUtil:
    @staticmethod
    def format_date(date):
        return date.strftime("%Y-%m-%d")

class CurrencyUtil:
    @staticmethod
    def format_currency(amount):
        return f"${amount:,.2f}"

def generate_financial_statements(start_date, end_date):
    # This is a placeholder function. You'll need to implement the actual logic.
    return {
        'income_statement': {},
        'balance_sheet': {}
    }

def get_budget(year):
    try:
        with open(f"{current_app.config['DATA_DIR']}/budget_{year}.csv", 'r') as f:
            reader = csv.DictReader(f)
            return {row['account_id']: float(row['amount']) for row in reader}
    except FileNotFoundError:
        return {}

def save_budget(year, budget_data):
    fieldnames = ['account_id', 'amount']
    with open(f"{current_app.config['DATA_DIR']}/budget_{year}.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for account_id, amount in budget_data.items():
            writer.writerow({'account_id': account_id, 'amount': amount})

def get_actual_data(year):
    accounts = get_accounts()
    journal_entries = get_journal_entries()
    actual_data = {account['id']: 0 for account in accounts}
    
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    for entry in journal_entries:
        entry_date = datetime.strptime(entry['date'], '%Y-%m-%d')
        if start_date <= entry_date <= end_date:
            amount = float(entry['amount'])
            debit_account = next((acc for acc in accounts if acc['id'] == entry['debit_account_id']), None)
            credit_account = next((acc for acc in accounts if acc['id'] == entry['credit_account_id']), None)
            
            if debit_account:
                if debit_account['category'] in ['Assets', 'Expenses']:
                    actual_data[debit_account['id']] += amount
                else:
                    actual_data[debit_account['id']] -= amount
            
            if credit_account:
                if credit_account['category'] in ['Assets', 'Expenses']:
                    actual_data[credit_account['id']] -= amount
                else:
                    actual_data[credit_account['id']] += amount
    
    return actual_data

def get_account_name(account_id):
    accounts = get_accounts()
    for account in accounts:
        if account['id'] == account_id:
            return account['name']
    return "Unknown Account"


def log_audit_trail(action, details):
    from app import db
    from models import AuditTrail
    
    audit_entry = AuditTrail(action=action, details=details)
    db.session.add(audit_entry)
    db.session.commit()