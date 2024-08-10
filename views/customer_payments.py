# File: views/customer_payments.py

from flask import render_template, request, jsonify
from models import CustomerPayment, Invoice, Customer
from utils import DateUtil, CurrencyUtil
from datetime import datetime

def customer_payments():
    if request.method == 'GET':
        payments = CustomerPayment.query.all()
        invoices = Invoice.query.filter_by(status='Unpaid').all()
        customers = Customer.query.all()
        return render_template('customer_payments.html', 
                               payments=payments, 
                               invoices=invoices,
                               customers=customers)
    elif request.method == 'POST':
        data = request.json
        invoice = Invoice.query.get(data['invoice_id'])
        new_payment = CustomerPayment(
            customer_id=invoice.customer_id,
            invoice_id=data['invoice_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            amount=data['amount'],
            payment_method=data['payment_method']
        )
        db.session.add(new_payment)
        
        # Update invoice status
        invoice.status = 'Paid' if data['amount'] >= invoice.total_amount else 'Partially Paid'
        
        db.session.commit()
        return jsonify({'success': True, 'id': new_payment.id})

def get_payment(payment_id):
    payment = CustomerPayment.query.get_or_404(payment_id)
    return jsonify({
        'id': payment.id,
        'customer': payment.customer.name,
        'invoice_number': payment.invoice.id,
        'date': DateUtil.format_date(payment.date),
        'amount': CurrencyUtil.format_currency(payment.amount),
        'payment_method': payment.payment_method
    })

def update_payment(payment_id):
    payment = CustomerPayment.query.get_or_404(payment_id)
    data = request.json
    payment.date = datetime.strptime(data['date'], '%Y-%m-%d')
    payment.amount = data['amount']
    payment.payment_method = data['payment_method']
    
    # Recalculate invoice status
    invoice = payment.invoice
    total_paid = sum(p.amount for p in invoice.payments)
    invoice.status = 'Paid' if total_paid >= invoice.total_amount else 'Partially Paid'
    
    db.session.commit()
    return jsonify({'success': True})

def delete_payment(payment_id):
    payment = CustomerPayment.query.get_or_404(payment_id)
    invoice = payment.invoice
    db.session.delete(payment)
    
    # Recalculate invoice status
    total_paid = sum(p.amount for p in invoice.payments if p.id != payment_id)
    invoice.status = 'Paid' if total_paid >= invoice.total_amount else 'Partially Paid'
    if total_paid == 0:
        invoice.status = 'Unpaid'
    
    db.session.commit()
    return jsonify({'success': True})

def get_customer_invoices(customer_id):
    invoices = Invoice.query.filter_by(customer_id=customer_id, status='Unpaid').all()
    return jsonify([{
        'id': i.id,
        'date': DateUtil.format_date(i.date),
        'due_date': DateUtil.format_date(i.due_date),
        'total_amount': CurrencyUtil.format_currency(i.total_amount),
        'remaining_amount': CurrencyUtil.format_currency(i.total_amount - sum(p.amount for p in i.payments))
    } for i in invoices])