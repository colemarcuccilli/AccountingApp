# File: views/vendor_payments.py (continued)

def delete_payment(payment_id):
    payment = VendorPayment.query.get_or_404(payment_id)
    bill = payment.bill
    db.session.delete(payment)
    
    # Recalculate bill status
    total_paid = sum(p.amount for p in bill.payments if p.id != payment_id)
    bill.status = 'Paid' if total_paid >= bill.total_amount else 'Partially Paid'
    if total_paid == 0:
        bill.status = 'Unpaid'
    
    db.session.commit()
    return jsonify({'success': True})

def get_vendor_bills(vendor_id):
    bills = Bill.query.filter_by(vendor_id=vendor_id, status='Unpaid').all()
    return jsonify([{
        'id': b.id,
        'bill_date': DateUtil.format_date(b.bill_date),
        'due_date': DateUtil.format_date(b.due_date),
        'total_amount': CurrencyUtil.format_currency(b.total_amount),
        'remaining_amount': CurrencyUtil.format_currency(b.total_amount - sum(p.amount for p in b.payments))
    } for b in bills])