# File: views/bills.py

from flask import render_template, request, jsonify
from models import Bill, Vendor, PurchaseTransaction
from utils import DateUtil, CurrencyUtil
from datetime import datetime

def bills():
    if request.method == 'GET':
        bills = Bill.query.all()
        vendors = Vendor.query.all()
        return render_template('bills.html', bills=bills, vendors=vendors)
    elif request.method == 'POST':
        data = request.json
        new_bill = Bill(
            vendor_id=data['vendor_id'],
            bill_date=datetime.strptime(data['bill_date'], '%Y-%m-%d'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'),
            total_amount=sum(item['amount'] for item in data['items']),
            status='Unpaid'
        )
        for item in data['items']:
            transaction = PurchaseTransaction.query.get(item['transaction_id'])
            new_bill.transactions.append(transaction)
        
        db.session.add(new_bill)
        db.session.commit()
        return jsonify({'success': True, 'id': new_bill.id})

def get_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return jsonify({
        'id': bill.id,
        'vendor': bill.vendor.name,
        'bill_date': DateUtil.format_date(bill.bill_date),
        'due_date': DateUtil.format_date(bill.due_date),
        'total_amount': CurrencyUtil.format_currency(bill.total_amount),
        'status': bill.status,
        'items': [{
            'transaction_id': t.id,
            'product': t.product.name,
            'quantity': t.quantity,
            'unit_price': CurrencyUtil.format_currency(t.unit_price),
            'amount': CurrencyUtil.format_currency(t.total_amount)
        } for t in bill.transactions]
    })

def update_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    data = request.json
    bill.vendor_id = data['vendor_id']
    bill.bill_date = datetime.strptime(data['bill_date'], '%Y-%m-%d')
    bill.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    bill.status = data['status']
    bill.transactions = []
    for item in data['items']:
        transaction = PurchaseTransaction.query.get(item['transaction_id'])
        bill.transactions.append(transaction)
    bill.total_amount = sum(t.total_amount for t in bill.transactions)
    db.session.commit()
    return jsonify({'success': True})

def delete_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'success': True})

def get_vendor_transactions(vendor_id):
    transactions = PurchaseTransaction.query.filter_by(vendor_id=vendor_id, bill_id=None).all()
    return jsonify([{
        'id': t.id,
        'date': DateUtil.format_date(t.date),
        'product': t.product.name,
        'quantity': t.quantity,
        'unit_price': CurrencyUtil.format_currency(t.unit_price),
        'amount': CurrencyUtil.format_currency(t.total_amount)
    } for t in transactions])