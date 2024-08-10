from flask import Blueprint, render_template
from utils import get_accounts, get_journal_entries, format_currency, update_account_balances
from datetime import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    update_account_balances()
    accounts = get_accounts()
    journal_entries = get_journal_entries()

    # Calculate total assets, liabilities, and equity
    assets = sum(float(account['balance']) for account in accounts if account['category'] == 'Assets')
    liabilities = sum(float(account['balance']) for account in accounts if account['category'] == 'Liabilities')
    equity = sum(float(account['balance']) for account in accounts if account['category'] == 'Equity')

    # Calculate total revenue and expenses
    revenue = sum(float(account['balance']) for account in accounts if account['category'] == 'Revenue')
    expenses = sum(float(account['balance']) for account in accounts if account['category'] == 'Expenses')

    # Get recent transactions
    recent_transactions = sorted(journal_entries, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)[:5]

    return render_template('dashboard.html', 
                           assets=format_currency(assets),
                           liabilities=format_currency(liabilities),
                           equity=format_currency(equity),
                           revenue=format_currency(revenue),
                           expenses=format_currency(expenses),
                           net_income=format_currency(revenue - expenses),
                           recent_transactions=recent_transactions)