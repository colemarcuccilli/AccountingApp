// File: static/js/purchase_transactions.js

document.addEventListener('DOMContentLoaded', function() {
    const newTransactionForm = document.getElementById('new-transaction-form');
    const editTransactionForm = document.getElementById('edit-transaction-form');
    const transactionsTable = document.getElementById('transactions-table');
    const modal = document.getElementById('transaction-modal');
    const vendorSelect = document.getElementById('vendor');
    const productSelect = document.getElementById('product');
    const quantityInput = document.getElementById('quantity');
    const unitPriceInput = document.getElementById('unit-price');
    const totalAmountInput = document.getElementById('total-amount');

    vendorSelect.addEventListener('change', loadVendorProducts);
    productSelect.addEventListener('change', updateUnitPrice);
    quantityInput.addEventListener('input', updateTotalAmount);
    unitPriceInput.addEventListener('input', updateTotalAmount);
    newTransactionForm.addEventListener('submit', addTransaction);
    editTransactionForm.addEventListener('submit', updateTransaction);
    transactionsTable.addEventListener('click', handleTableActions);

    function loadVendorProducts() {
        const vendorId = vendorSelect.value;
        productSelect.innerHTML = '<option value="">Select a product</option>';
        productSelect.disabled = true;
        
        if (vendorId) {
            fetch(`/vendor-products/${vendorId}`)
                .then(response => response.json())
                .then(products => {
                    products.forEach(product => {
                        const option = document.createElement('option');
                        option.value = product.id;
                        option.textContent = `${product.name} (${product.sku})`;
                        option.dataset.price = product.default_price;
                        productSelect.appendChild(option);
                    });
                    productSelect.disabled = false;
                });
        }
    }

    function updateUnitPrice() {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        if (selectedOption.dataset.price) {
            unitPriceInput.value = parseFloat(selectedOption.dataset.price).toFixed(2);
            updateTotalAmount();
        }
    }

    function updateTotalAmount() {
        const quantity = parseFloat(quantityInput.value) || 0;
        const unitPrice = parseFloat(unitPriceInput.value) || 0;
        totalAmountInput.value = (quantity * unitPrice).toFixed(2);
    }

    function addTransaction(e) {
        e.preventDefault();
        const formData = {
            vendor_id: vendorSelect.value,
            date: document.getElementById('date').value,
            product_id: productSelect.value,
            quantity: quantityInput.value,
            unit_price: unitPriceInput.value
        };

        fetch('/purchase-transactions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Refresh to show new transaction
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function handleTableActions(e) {
        if (e.target.classList.contains('edit-btn')) {
            const row = e.target.closest('tr');
            const id = row.dataset.id;
            editTransaction(id);
        } else if (e.target.classList.contains('delete-btn')) {
            const row = e.target.closest('tr');
            const id = row.dataset.id;
            deleteTransaction(id);
        }
    }

    function editTransaction(id) {
        fetch(`/purchase-transactions/${id}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('edit-transaction-id').value = data.id;
                document.getElementById('edit-vendor').value = data.vendor_id;
                document.getElementById('edit-date').value = data.date;
                loadVendorProductsForEdit(data.vendor_id, data.product_id);
                document.getElementById('edit-quantity').value = data.quantity;
                document.getElementById('edit-unit-price').value = data.unit_price.replace(/[^0-9.]/g, '');
                document.getElementById('edit-total-amount').value = data.total_amount;
                modal.style.display = 'block';
            });
    }

    function loadVendorProductsForEdit(vendorId, productId) {
        const editProductSelect = document.getElementById('edit-product');
        editProductSelect.innerHTML = '<option value="">Select a product</option>';
        
        fetch(`/vendor-products/${vendorId}`)
            .then(response => response.json())
            .then(products => {
                products.forEach(product => {
                    const option = document.createElement('option');
                    option.value = product.id;
                    option.textContent = `${product.name} (${product.sku})`;
                    option.dataset.price = product.default_price;
                    editProductSelect.appendChild(option);
                });
                editProductSelect.value = productId;
            });
    }

    function updateTransaction(e) {
        e.preventDefault();
        const id = document.getElementById('edit-transaction-id').value;
        const formData = {
            vendor_id: document.getElementById('edit-vendor').value,
            date: document.getElementById('edit-date').value,
            product_id: document.getElementById('edit-product').value,
            quantity: document.getElementById('edit-quantity').value,
            unit_price: document.getElementById('edit-unit-price').value
        };

        fetch(`/purchase-transactions/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                location.reload();  // Refresh to show updated transaction
            }
        })
        .catch((error) =>