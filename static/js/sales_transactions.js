// File: static/js/sales_transactions.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('new-transaction-form');
    const table = document.getElementById('transactions-table');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = {
            customer_id: document.getElementById('customer').value,
            date: document.getElementById('date').value,
            product_id: document.getElementById('product').value,
            quantity: document.getElementById('quantity').value,
            unit_price: document.getElementById('unit-price').value
        };

        fetch('/sales-transactions', {
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
    });

    table.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-btn')) {
            const row = e.target.closest('tr');
            const id = row.dataset.id;
            editTransaction(id);
        } else if (e.target.classList.contains('delete-btn')) {
            const row = e.target.closest('tr');
            const id = row.dataset.id;
            deleteTransaction(id);
        }
    });

    function editTransaction(id) {
        fetch(`/sales-transactions/${id}`)
            .then(response => response.json())
            .then(data => {
                // Populate form with existing data
                document.getElementById('customer').value = data.customer_id;
                document.getElementById('date').value = data.date;
                document.getElementById('product').value = data.product_id;
                document.getElementById('quantity').value = data.quantity;
                document.getElementById('unit-price').value = data.unit_price;

                // Change form submission to update instead of create
                form.onsubmit = function(e) {
                    e.preventDefault();
                    updateTransaction(id);
                };
            });
    }

    function updateTransaction(id) {
        const formData = {
            customer_id: document.getElementById('customer').value,
            date: document.getElementById('date').value,
            product_id: document.getElementById('product').value,
            quantity: document.getElementById('quantity').value,
            unit_price: document.getElementById('unit-price').value
        };

        fetch(`/sales-transactions/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Refresh to show updated transaction
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function deleteTransaction(id) {
        if (confirm('Are you sure you want to delete this transaction?')) {
            fetch(`/sales-transactions/${id}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();  // Refresh to remove deleted transaction
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }
});