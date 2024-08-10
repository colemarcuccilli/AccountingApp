// File: static/js/customer_payments.js

document.addEventListener('DOMContentLoaded', function() {
    const newPaymentForm = document.getElementById('new-payment-form');
    const editPaymentForm = document.getElementById('edit-payment-form');
    const paymentsTable = document.getElementById('payments-table');
    const modal = document.getElementById('payment-modal');
    const customerSelect = document.getElementById('customer');
    const invoiceSelect = document.getElementById('invoice');

    customerSelect.addEventListener('change', loadCustomerInvoices);
    newPaymentForm.addEventListener('submit', recordPayment);
    editPaymentForm.addEventListener('submit', updatePayment);
    paymentsTable.addEventListener('click', handleTableActions);

    function loadCustomerInvoices() {
        const customerId = customerSelect.value;
        invoiceSelect.innerHTML = '<option value="">Select an invoice</option>';
        invoiceSelect.disabled = true;
        
        if (customerId) {
            fetch(`/customer-invoices/${customerId}`)
                .then(response => response.json())
                .then(invoices => {
                    invoices.forEach(invoice => {
                        const option = document.createElement('option');
                        option.value = invoice.id;
                        option.textContent = `Invoice #${invoice.id} - Due: ${invoice.due_date} - Remaining: ${invoice.remaining_amount}`;
                        invoiceSelect.appendChild(option);
                    });
                    invoiceSelect.disabled = false;
                });
        }
    }

    function recordPayment(e) {
        e.preventDefault();
        const formData = {
            invoice_id: invoiceSelect.value,
            date: document.getElementById('date').value,
            amount: document.getElementById('amount').value,
            payment_method: document.getElementById('payment-method').value
        };

        fetch('/customer-payments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Refresh to show new payment
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
            editPayment(id);
        } else if (e.target.classList.contains('delete-btn')) {
            const row = e.target.closest('tr');
            const id = row.dataset.id;
            deletePayment(id);
        }
    }

    function editPayment(id) {
        fetch(`/customer-payments/${id}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('edit-payment-id').value = data.id;
                document.getElementById('edit-date').value = data.date;
                document.getElementById('edit-amount').value = data.amount.replace(/[^0-9.]/g, '');
                document.getElementById('edit-payment-method').value = data.payment_method;
                modal.style.display = 'block';
            });
    }

    function updatePayment(e) {
        e.preventDefault();
        const id = document.getElementById('edit-payment-id').value;
        const formData = {
            date: document.getElementById('edit-date').value,
            amount: document.getElementById('edit-amount').value,
            payment_method: document.getElementById('edit-payment-method').value
        };

        fetch(`/customer-payments/${id}`, {
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
                location.reload();  // Refresh to show updated payment
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function deletePayment(id) {
        if (confirm('Are you sure you want to delete this payment?')) {
            fetch(`/customer-payments/${id}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();  // Refresh to remove deleted payment
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }

    // Close the modal when clicking on <span> (x)
    document.querySelector('.close').onclick = function() {
        modal.style.display = 'none';
    }

    // Close the modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});