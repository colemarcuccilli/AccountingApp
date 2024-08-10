# File: views/invoices.py

from flask import render_template, request, jsonify
from models import Invoice, SalesTransaction, Customer
from utils import DateUtil, CurrencyUtil, PDFGenerator
from datetime import datetime

def invoices():
    if request.method == 'GET':
        invoices = Invoice.query.all()
        customers = Customer.query.all()
        return render_template('invoices.html', 
                               invoices=invoices, 
                               customers=customers)
    elif request.method == 'POST':
        data = request.json
        new_invoice = Invoice(
            customer_id=data['customer_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'),
            total_amount=sum(item['amount'] for item in data['items']),
            status='Unpaid'
        )
        for item in data['items']:
            transaction = SalesTransaction.query.get(item['transaction_id'])
            new_invoice.transactions.append(transaction)
        
        db.session.add(new_invoice)
        db.session.commit()
        return jsonify({'success': True, 'id': new_invoice.id})

def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify({
        'id': invoice.id,
        'customer': invoice.customer.name,
        'date': DateUtil.format_date(invoice.date),
        'due_date': DateUtil.format_date(invoice.due_date),
        'total_amount': CurrencyUtil.format_currency(invoice.total_amount),
        'status': invoice.status,
        'items': [{
            'transaction_id': t.id,
            'product': t.product.name,
            'quantity': t.quantity,
            'unit_price': CurrencyUtil.format_currency(t.unit_price),
            'amount': CurrencyUtil.format_currency(t.total_amount)
        } for t in invoice.transactions]
    })

def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.json
    invoice.customer_id = data['customer_id']
    invoice.date = datetime.strptime(data['date'], '%Y-%m-%d')
    invoice.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    invoice.status = data['status']
    invoice.transactions = []
    for item in data['items']:
        transaction = SalesTransaction.query.get(item['transaction_id'])
        invoice.transactions.append(transaction)
    invoice.total_amount = sum(t.total_amount for t in invoice.transactions)
    db.session.commit()
    return jsonify({'success': True})

def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'success': True})

def generate_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    pdf = PDFGenerator.generate_invoice(invoice)
    return pdf, 200, {'Content-Type': 'application/pdf'}

def get_customer_transactions(customer_id):
    transactions = SalesTransaction.query.filter_by(customer_id=customer_id, invoice_id=None).all()
    return jsonify([{
        'id': t.id,
        'date': DateUtil.format_date(t.date),
        'product': t.product.name,
        'quantity': t.quantity,
        'unit_price': CurrencyUtil.format_currency(t.unit_price),
        'amount': CurrencyUtil.format_currency(t.total_amount)
    } for t in transactions])