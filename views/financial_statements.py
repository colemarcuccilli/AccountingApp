from flask import Blueprint, render_template, request, jsonify
from utils import get_accounts, get_journal_entries, format_currency
from datetime import datetime

bp = Blueprint('financial_statements', __name__, url_prefix='/financial-statements')

@bp.route('/')
def index():
    return render_template('financial_statements.html')

@bp.route('/income-statement')
def income_statement():
    end_date = datetime.strptime(request.args.get('end_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
    start_date = datetime.strptime(request.args.get('start_date', end_date.replace(day=1).strftime('%Y-%m-%d')), '%Y-%m-%d')

    accounts = get_accounts()
    journal_entries = get_journal_entries()

    revenue = []
    total_revenue = 0
    expenses = []
    total_expenses = 0

    for account in accounts:
        if account['type'] == 'Revenue':
            amount = sum(float(entry['amount']) for entry in journal_entries 
                         if entry['credit_account_id'] == account['id']
                         and start_date <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date)
            if amount > 0:
                revenue.append({'account': account['name'], 'amount': format_currency(amount)})
                total_revenue += amount
        elif account['type'] == 'Expense':
            amount = sum(float(entry['amount']) for entry in journal_entries 
                         if entry['debit_account_id'] == account['id']
                         and start_date <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date)
            if amount > 0:
                expenses.append({'account': account['name'], 'amount': format_currency(amount)})
                total_expenses += amount

    net_income = total_revenue - total_expenses

    return render_template('income_statement.html',
                           start_date=start_date.strftime('%Y-%m-%d'),
                           end_date=end_date.strftime('%Y-%m-%d'),
                           revenue=revenue,
                           total_revenue=format_currency(total_revenue),
                           expenses=expenses,
                           total_expenses=format_currency(total_expenses),
                           net_income=format_currency(net_income))

@bp.route('/balance-sheet')
def balance_sheet():
    as_of_date = datetime.strptime(request.args.get('as_of_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
    print(f"As of date: {as_of_date}")

    accounts = get_accounts()
    journal_entries = get_journal_entries()
    print(f"Number of accounts: {len(accounts)}")
    print(f"Number of journal entries: {len(journal_entries)}")

    assets = []
    liabilities = []
    equity = []
    total_assets = 0
    total_liabilities = 0
    total_equity = 0

    for account in accounts:
        balance = sum(float(entry['amount']) for entry in journal_entries
                      if entry['debit_account_id'] == account['id'] and datetime.strptime(entry['date'], '%Y-%m-%d') <= as_of_date) - \
                  sum(float(entry['amount']) for entry in journal_entries
                      if entry['credit_account_id'] == account['id'] and datetime.strptime(entry['date'], '%Y-%m-%d') <= as_of_date)
        
        print(f"Account: {account['name']}, Category: {account['category']}, Balance: {balance}")

        if account['category'] == 'Assets':
            assets.append({'account': account['name'], 'amount': format_currency(balance)})
            total_assets += balance
        elif account['category'] == 'Liabilities':
            liabilities.append({'account': account['name'], 'amount': format_currency(abs(balance))})
            total_liabilities += abs(balance)
        elif account['category'] == 'Equity':
            equity.append({'account': account['name'], 'amount': format_currency(abs(balance))})
            total_equity += abs(balance)

    balance_sheet = {
        'assets': assets,
        'total_assets': format_currency(total_assets),
        'liabilities': liabilities,
        'total_liabilities': format_currency(total_liabilities),
        'equity': equity,
        'total_equity': format_currency(total_equity)
    }

    print(f"Total Assets: {total_assets}")
    print(f"Total Liabilities: {total_liabilities}")
    print(f"Total Equity: {total_equity}")

    return render_template('balance_sheet.html', balance_sheet=balance_sheet, as_of_date=as_of_date.strftime('%Y-%m-%d'))