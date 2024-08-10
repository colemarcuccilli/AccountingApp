# File: views/accounts_payable.py (continued)

def get_aging_summary():
    as_of_date = datetime.now()
    vendors = Vendor.query.all()
    
    aging_summary = []
    for vendor in vendors:
        bills = Bill.query.filter_by(vendor_id=vendor.id).all()
        current = overdue_30 = overdue_60 = overdue_90 = 0
        
        for bill in bills:
            payments = VendorPayment.query.filter_by(bill_id=bill.id).all()
            total_paid = sum(payment.amount for payment in payments)
            remaining = bill.total_amount - total_paid
            
            if remaining > 0:
                days_overdue = (as_of_date - bill.due_date).days
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
                'vendor_name': vendor.name,
                'current': CurrencyUtil.format_currency(current),
                '1-30_days': CurrencyUtil.format_currency(overdue_30),
                '31-60_days': CurrencyUtil.format_currency(overdue_60),
                '60+_days': CurrencyUtil.format_currency(overdue_90),
                'total': CurrencyUtil.format_currency(current + overdue_30 + overdue_60 + overdue_90)
            })
    
    return jsonify(aging_summary)

def get_payment_efficiency():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    bills = Bill.query.filter(Bill.bill_date.between(start_date, end_date)).all()
    total_billed = sum(bill.total_amount for bill in bills)
    total_paid = sum(
        payment.amount 
        for bill in bills 
        for payment in bill.payments 
        if payment.date <= end_date
    )
    
    efficiency = (total_paid / total_billed * 100) if total_billed > 0 else 0
    
    return jsonify({
        'total_billed': CurrencyUtil.format_currency(total_billed),
        'total_paid': CurrencyUtil.format_currency(total_paid),
        'efficiency': f"{efficiency:.2f}%"
    })