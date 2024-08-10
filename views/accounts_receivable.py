# File: views/accounts_receivable.py

from flask import render_template, request, jsonify
from models import Invoice, CustomerPayment, Customer
from utils import DateUtil, CurrencyUtil
from datetime import datetime, timedelta

def accounts_receivable():
    customers = Customer.query.all()
    return render_template('accounts_receivable.html', customers=customers)

def get_ar_data():
    data = request.args
    customer_id = data.get('customer_id')
    as_of_date = datetime.strptime(data.get('as_of_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
    
    query = Invoice.query.filter(Invoice.date <= as_of_date)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    
    invoices = query.all()
    
    ar_data = []
    for invoice in invoices:
        payments = CustomerPayment.query.filter(CustomerPayment.invoice_id == invoice.id, 
                                                CustomerPayment.date <= as_of_date).all()
        total_paid = sum(payment.amount for payment in payments)
        remaining = invoice.total_amount - total_paid
        
        if remaining > 0:
            days_overdue = (as_of_date - invoice.due_date).days if as_of_date > invoice.due_date else 0
            ar_data.append({
                'invoice_id': invoice.id,
                'customer_name': invoice.customer.name,
                'invoice_date': DateUtil.format_date(invoice.date),
                'due_date': DateUtil.format_date(invoice.due_date),
                'total_amount': CurrencyUtil.format_currency(invoice.total_amount),
                'remaining': CurrencyUtil.format_currency(remaining),
                'days_overdue': days_overdue,
                'status': get_invoice_status(invoice, remaining, days_overdue)
            })
    
    return jsonify(ar_data)

def get_invoice_status(invoice, remaining, days_overdue):
    if remaining == 0:
        return 'Paid'
    elif days_overdue > 90:
        return 'Severely Overdue'
    elif days_overdue > 60:
        return 'Very Overdue'
    elif days_overdue > 30:
        return 'Overdue'
    elif days_overdue > 0:
        return 'Slightly Overdue'
    else:
        return 'Current'

def get_aging_summary():
    as_of_date = datetime.now()
    customers = Customer.query.all()
    
    aging_summary = []
    for customer in customers:
        invoices = Invoice.query.filter_by(customer_id=customer.id).all()
        current = overdue_30 = overdue_60 = overdue_90 = 0
        
        for invoice in invoices:
            payments = CustomerPayment.query.filter_by(invoice_id=invoice.id).all()
            total_paid = sum(payment.amount for payment in payments)
            remaining = invoice.total_amount - total_paid
            
            if remaining > 0:
                days_overdue = (as_of_date - invoice.due_date).days
                if days_overdue <= 0:
                    current += remaining
                elif days_overdue <= 30:
                    overdue_30 += remaining
                elif days_overdue <= 60:
                    overdue_60 += remaining
                else:
                    overdue_90 += remaining
        
        if current or overdue_30 or overdue_60 or overdue_90:
            aging_summary.append({
                'customer_name': customer.name,
                'current': CurrencyUtil.format_currency(current),
                '1-30_days': CurrencyUtil.format_currency(overdue_30),
                '31-60_days': CurrencyUtil.format_currency(overdue_60),
                '60+_days': CurrencyUtil.format_currency(overdue_90),
                'total': CurrencyUtil.format_currency(current + overdue_30 + overdue_60 + overdue_90)
            })
    
    return jsonify(aging_summary)

def get_collection_efficiency():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    invoices = Invoice.query.filter(Invoice.date.between(start_date, end_date)).all()
    total_invoiced = sum(invoice.total_amount for invoice in invoices)
    total_collected = sum(
        payment.amount 
        for invoice in invoices 
        for payment in invoice.payments 
        if payment.date <= end_date
    )
    
    efficiency = (total_collected / total_invoiced * 100) if total_invoiced > 0 else 0
    
    return jsonify({
        'total_invoiced': CurrencyUtil.format_currency(total_invoiced),
        'total_collected': CurrencyUtil.format_currency(total_collected),
        'efficiency': f"{efficiency:.2f}%"
    })