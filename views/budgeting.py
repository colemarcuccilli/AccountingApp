from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_accounts, get_budget, save_budget, format_currency
from datetime import datetime

bp = Blueprint('budgeting', __name__, url_prefix='/budgeting')

@bp.route('/')
def index():
    current_year = datetime.now().year
    budget = get_budget(current_year)
    accounts = get_accounts()
    
    # Group accounts by category
    account_categories = {}
    for account in accounts:
        if account['category'] not in account_categories:
            account_categories[account['category']] = []
        account_categories[account['category']].append(account)
    
    return render_template('budgeting.html', budget=budget, account_categories=account_categories, current_year=current_year)

@bp.route('/set', methods=['POST'])
def set_budget():
    year = int(request.form['year'])
    budget_data = {}
    
    try:
        for key, value in request.form.items():
            if key.startswith('budget_'):
                account_id = key.split('_')[1]
                budget_data[account_id] = float(value) if value else 0
        
        save_budget(year, budget_data)
        flash('Budget has been set successfully', 'success')
    except ValueError as e:
        flash(f'Error setting budget: {str(e)}', 'error')
    except Exception as e:
        flash(f'An unexpected error occurred: {str(e)}', 'error')
    
    return redirect(url_for('budgeting.index'))

@bp.route('/compare')
def compare_budget():
    year = int(request.args.get('year', datetime.now().year))
    budget = get_budget(year)
    actual = get_actual_data(year)
    
    comparison = {}
    for account_id in set(budget.keys()) | set(actual.keys()):
        comparison[account_id] = {
            'budgeted': budget.get(account_id, 0),
            'actual': actual.get(account_id, 0),
            'variance': actual.get(account_id, 0) - budget.get(account_id, 0)
        }
    
    return render_template('budget_comparison.html', comparison=comparison, year=year)