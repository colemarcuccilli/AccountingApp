import random
from datetime import datetime, timedelta
from app import app
from utils import (
    get_predefined_accounts, add_account, add_journal_entry,
    save_budget, get_accounts, update_account_balances
)

def generate_test_data():
    with app.app_context():
        # Generate accounts
        generate_accounts()

        # Generate journal entries
        generate_journal_entries()

        # Generate budget
        generate_budget()

        # Update account balances
        update_account_balances()

def generate_accounts():
    predefined_accounts = get_predefined_accounts()
    for category, subcategories in predefined_accounts.items():
        for subcategory, accounts in subcategories.items():
            for account_code, account_name in accounts:
                add_account(account_code, account_name, category, subcategory)

def generate_journal_entries():
    accounts = get_accounts()
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    num_entries = 1000
    for _ in range(num_entries):
        date = start_date + timedelta(days=random.randint(0, 364))
        description = f"Test transaction {_+1}"
        debit_account = random.choice(accounts)
        credit_account = random.choice([acc for acc in accounts if acc['id'] != debit_account['id']])
        amount = round(random.uniform(10, 10000), 2)
        
        add_journal_entry(
            date.strftime('%Y-%m-%d'),
            description,
            debit_account['id'],
            credit_account['id'],
            str(amount)
        )

def generate_budget():
    accounts = get_accounts()
    year = 2024
    budget_data = {}
    
    for account in accounts:
        if account['category'] in ['Revenue', 'Expenses']:
            budget_data[account['id']] = round(random.uniform(1000, 100000), 2)
    
    save_budget(year, budget_data)

if __name__ == "__main__":
    generate_test_data()
    print("Test data generated successfully!")