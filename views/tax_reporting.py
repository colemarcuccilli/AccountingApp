from flask import Blueprint, render_template, request
from utils import get_accounts, get_journal_entries, format_currency
from datetime import datetime

bp = Blueprint('tax_reporting', __name__, url_prefix='/tax-reporting')

@bp.route('/')
def index():
    return render_template('tax_reporting.html')

@bp.route('/generate', methods=['POST'])
def generate_report():
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    
    accounts = get_accounts()
    entries = get_journal_entries()
    
    revenue = sum(float(entry['amount']) for entry in entries 
                  if any(acc['id'] == entry['credit_account_id'] for acc in accounts if acc['category'] == 'Revenue')
                  and start_date <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date)
    
    expenses = sum(float(entry['amount']) for entry in entries 
                   if any(acc['id'] == entry['debit_account_id'] for acc in accounts if acc['category'] == 'Expenses')
                   and start_date <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date)
    
    net_income = revenue - expenses
    estimated_tax = net_income * 0.3  # Simplified tax calculation, adjust as needed
    
    report = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'revenue': format_currency(revenue),
        'expenses': format_currency(expenses),
        'net_income': format_currency(net_income),
        'estimated_tax': format_currency(estimated_tax)
    }
    
    return render_template('tax_report.html', report=report)