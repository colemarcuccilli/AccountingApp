from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_accounts, add_account, update_account, delete_account, format_currency, update_account_balances, get_predefined_accounts

bp = Blueprint('chart_of_accounts', __name__, url_prefix='/chart-of-accounts')

@bp.route('/')
def index():
    update_account_balances()
    accounts = get_accounts()
    for account in accounts:
        account['balance'] = format_currency(float(account.get('balance', 0)))
    
    structured_accounts = {}
    for account in accounts:
        category = account.get('category', 'Uncategorized')
        subcategory = account.get('subcategory', 'Uncategorized')
        if category not in structured_accounts:
            structured_accounts[category] = {}
        if subcategory not in structured_accounts[category]:
            structured_accounts[category][subcategory] = []
        structured_accounts[category][subcategory].append(account)

    return render_template('chart_of_accounts.html', structured_accounts=structured_accounts)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        account_code = request.form['account_code']
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        add_account(account_code, name, category, subcategory)
        flash('Account added successfully', 'success')
        return redirect(url_for('chart_of_accounts.index'))
    
    predefined_accounts = get_predefined_accounts()
    return render_template('account_form.html', title='Add Account', predefined_accounts=predefined_accounts)

@bp.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    accounts = get_accounts()
    account = next((acc for acc in accounts if acc['id'] == id), None)
    if account is None:
        flash('Account not found', 'error')
        return redirect(url_for('chart_of_accounts.index'))
    
    if request.method == 'POST':
        account['name'] = request.form['name']
        account['category'] = request.form['category']
        account['subcategory'] = request.form['subcategory']
        update_account(id, account)
        flash('Account updated successfully', 'success')
        return redirect(url_for('chart_of_accounts.index'))
    
    predefined_accounts = get_predefined_accounts()
    return render_template('account_form.html', account=account, title='Edit Account', predefined_accounts=predefined_accounts)

@bp.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    delete_account(id)
    flash('Account deleted successfully', 'success')
    return redirect(url_for('chart_of_accounts.index'))