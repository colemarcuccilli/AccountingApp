# File: views/transactions.py

from flask import render_template, request, jsonify
from models import SalesTransaction, Customer, Product
from utils import DateUtil, CurrencyUtil
from datetime import datetime

def sales_transactions():
    if request.method == 'GET':
        transactions = SalesTransaction.query.all()
        customers = Customer.query.all()
        products = Product.query.all()
        return render_template('sales_transactions.html', 
                               transactions=transactions, 
                               customers=customers, 
                               products=products)
    elif request.method == 'POST':
        data = request.json
        new_transaction = SalesTransaction(
            customer_id=data['customer_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            product_id=data['product_id'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            total_amount=data['quantity'] * data['unit_price']
        )
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'success': True, 'id': new_transaction.id})

def get_transaction(transaction_id):
    transaction = SalesTransaction.query.get_or_404(transaction_id)
    return jsonify({
        'id': transaction.id,
        'customer': transaction.customer.name,
        'date': DateUtil.format_date(transaction.date),
        'product': transaction.product.name,
        'quantity': transaction.quantity,
        'unit_price': CurrencyUtil.format_currency(transaction.unit_price),
        'total_amount': CurrencyUtil.format_currency(transaction.total_amount)
    })

def update_transaction(transaction_id):
    transaction = SalesTransaction.query.get_or_404(transaction_id)
    data = request.json
    transaction.customer_id = data['customer_id']
    transaction.date = datetime.strptime(data['date'], '%Y-%m-%d')
    transaction.product_id = data['product_id']
    transaction.quantity = data['quantity']
    transaction.unit_price = data['unit_price']
    transaction.total_amount = data['quantity'] * data['unit_price']
    db.session.commit()
    return jsonify({'success': True})

def delete_transaction(transaction_id):
    transaction = SalesTransaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'success': True})