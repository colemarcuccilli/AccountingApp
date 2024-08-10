# File: views/purchase_transactions.py

from flask import render_template, request, jsonify
from models import PurchaseTransaction, Vendor, Product, Inventory
from utils import DateUtil, CurrencyUtil
from datetime import datetime

def purchase_transactions():
    if request.method == 'GET':
        transactions = PurchaseTransaction.query.all()
        vendors = Vendor.query.all()
        products = Product.query.all()
        return render_template('purchase_transactions.html', 
                               transactions=transactions, 
                               vendors=vendors,
                               products=products)
    elif request.method == 'POST':
        data = request.json
        new_transaction = PurchaseTransaction(
            vendor_id=data['vendor_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            product_id=data['product_id'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            total_amount=data['quantity'] * data['unit_price']
        )
        db.session.add(new_transaction)
        
        # Update inventory
        inventory = Inventory.query.filter_by(product_id=data['product_id']).first()
        if inventory:
            inventory.quantity += data['quantity']
        else:
            new_inventory = Inventory(product_id=data['product_id'], quantity=data['quantity'])
            db.session.add(new_inventory)
        
        db.session.commit()
        return jsonify({'success': True, 'id': new_transaction.id})

def get_transaction(transaction_id):
    transaction = PurchaseTransaction.query.get_or_404(transaction_id)
    return jsonify({
        'id': transaction.id,
        'vendor': transaction.vendor.name,
        'date': DateUtil.format_date(transaction.date),
        'product': transaction.product.name,
        'quantity': transaction.quantity,
        'unit_price': CurrencyUtil.format_currency(transaction.unit_price),
        'total_amount': CurrencyUtil.format_currency(transaction.total_amount)
    })

def update_transaction(transaction_id):
    transaction = PurchaseTransaction.query.get_or_404(transaction_id)
    data = request.json
    
    # Calculate the change in quantity
    quantity_change = data['quantity'] - transaction.quantity
    
    transaction.vendor_id = data['vendor_id']
    transaction.date = datetime.strptime(data['date'], '%Y-%m-%d')
    transaction.product_id = data['product_id']
    transaction.quantity = data['quantity']
    transaction.unit_price = data['unit_price']
    transaction.total_amount = data['quantity'] * data['unit_price']
    
    # Update inventory
    inventory = Inventory.query.filter_by(product_id=data['product_id']).first()
    if inventory:
        inventory.quantity += quantity_change
    else:
        new_inventory = Inventory(product_id=data['product_id'], quantity=quantity_change)
        db.session.add(new_inventory)
    
    db.session.commit()
    return jsonify({'success': True})

def delete_transaction(transaction_id):
    transaction = PurchaseTransaction.query.get_or_404(transaction_id)
    
    # Update inventory
    inventory = Inventory.query.filter_by(product_id=transaction.product_id).first()
    if inventory:
        inventory.quantity -= transaction.quantity
        if inventory.quantity < 0:
            inventory.quantity = 0
    
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'success': True})

def get_vendor_products(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    products = Product.query.filter_by(vendor_id=vendor_id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'default_price': CurrencyUtil.format_currency(p.default_price)
    } for p in products])