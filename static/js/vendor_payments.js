// File: static/js/vendor_payments.js

document.addEventListener('DOMContentLoaded', function() {
    const newPaymentForm = document.getElementById('new-payment-form');
    const editPaymentForm = document.getElementById('edit-payment-form');
    const paymentsTable = document.getElementById('payments-table');
    const modal = document.getElementById('payment-modal');
    const vendorSelect = document.getElementById('vendor');
    const billSelect = document.getElementById('bill');

    vendorSelect.addEventListener('change', loadVendorBills);
    newPaymentForm.addEventListener('submit', recordPayment);
    editPaymentForm.addEventListener('submit', updatePayment);
    paymentsTable.addEventListener('click', handleTableActions);

    function loadVendorBills() {
        const vendorId = vendorSelect.value;
        billSelect.innerHTML = '<option value="">Select a bill</option>';
        billSelect.disabled = true;
        
        if (vendorId) {
            fetch(`/vendor-bills/${vendorId}`)
                .then(response => response.json())
                .then(bills => {
                    bills.forEach(bill => {
                        const option = document.createElement('option');
                        option.value = bill.id;
                        option.textContent = `Bill #${bill.id} - Due: ${bill.due_date} - Remaining: ${bill.remaining_amount}`;
                        billSelect.appendChild(option);
                    });
                    billSelect.disabled = false;
                });
        }
    }

    function recordPayment(e) {
        e.preventDefault();
        const formData = {
            bill_id: billSelect.value,
            date: document.getElementById('date').value,
            amount: document.getElementById('amount').value,
            payment_method: document.getElementById('payment-method').value
        };

        fetch('/vendor-payments', {
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
        fetch(`/vendor-payments/${id}`)
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

        fetch(`/vendor-payments/${id}`, {
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
            fetch(`/vendor-payments/${id}`, {
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