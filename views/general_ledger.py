from flask import Blueprint, render_template, request, jsonify
from utils import DateUtil, CurrencyUtil

bp = Blueprint('general_ledger', __name__, url_prefix='/general-ledger')

@bp.route('/')
def index():
    accounts = Account.query.all()
    return render_template('general_ledger.html', accounts=accounts)

@bp.route('/data')
def get_ledger_data():
    account_id = request.args.get('account_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Transaction.query
    if account_id:
        query = query.filter_by(account_id=account_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.order_by(Transaction.date).all()
    
    ledger_data = []
    balance = 0
    for transaction in transactions:
        if transaction.type == 'debit':
            balance += transaction.amount
        else:
            balance -= transaction.amount
        
        ledger_data.append({
            'date': DateUtil.format_date(transaction.date),
            'description': transaction.description,
            'debit': CurrencyUtil.format_currency(transaction.amount) if transaction.type == 'debit' else '',
            'credit': CurrencyUtil.format_currency(transaction.amount) if transaction.type == 'credit' else '',
            'balance': CurrencyUtil.format_currency(balance)
        })
    
    return jsonify(ledger_data)