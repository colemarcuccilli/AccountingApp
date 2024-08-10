// File: static/js/invoices.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('new-invoice-form');
    const table = document.getElementById('invoices-table');
    const modal = document.getElementById('invoice-modal');
    const addItemButton = document.getElementById('add-item');
    const customerSelect = document.getElementById('customer');

    customerSelect.addEventListener('change', loadCustomerTransactions);
    addItemButton.addEventListener('click', addInvoiceItem);
    form.addEventListener('submit', createInvoice);
    table.addEventListener('click', handleTableActions);

    function loadCustomerTransactions() {
        const customerId = customerSelect.value;
        fetch(`/customer-transactions/${customerId}`)
            .then(response => response.json())
            .then(transactions => {
                const itemsContainer = document.getElementById('invoice-items');
                itemsContainer.innerHTML = '';
                transactions.forEach(transaction => {
                    addInvoiceItem(transaction);
                });
            });
    }

    function addInvoiceItem(transaction = null) {
        const itemsContainer = document.getElementById('invoice-items');
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('invoice-item');
        itemDiv.innerHTML = `
            <select class="transaction-select" ${transaction ? 'disabled' : ''}>
                ${transaction ? `<option value="${transaction.id}">${transaction.product} - ${transaction.amount}</option>` : ''}
            </select>
            <input type="number" class="item-quantity" value="${transaction ? transaction.quantity : 1}" min="1" ${transaction ? 'readonly' : ''}>
            <span class="item-amount">${transaction ? transaction.amount : ''}</span>
            <button type="button" class="remove-item">Remove</button>
        `;
        itemsContainer.appendChild(itemDiv);

        itemDiv.querySelector('.remove-item').addEventListener('click', function() {
            itemsContainer.removeChild(itemDiv);
        });
    }

    function createInvoice(e) {
        e.preventDefault();
        const formData = {
            customer_id: document.getElementById('customer').value,
            date: document.getElementById('date').value,
            due_date: document.getElementById('due-date').value,
            items: Array.from(document.querySelectorAll('.invoice-item')).map(item => ({
                transaction_id: item.querySelector('.transaction-select').value,
                quantity: item.querySelector('.item-quantity').value
            }))
        };

        fetch('/invoices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Refresh to show new invoice
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function handleTableActions(e) {
        const action = e.target.classList[0];
        const row = e.target.closest('tr');
        const id = row.dataset.id;

        switch(action) {
            case 'view-btn':
                viewInvoice(id);
                break;
            case 'edit-btn':
                editInvoice(id);
                break;
            case 'delete-btn':
                deleteInvoice(id);
                break;
            case 'pdf-btn':
                generatePDF(id);
                break;
        }
    }

    function viewInvoice(id) {
        fetch(`/invoices/${id}`)
            .then(response => response.json())
            .then(data => {
                const detailsDiv = document.getElementById('invoice-details');
                detailsDiv.innerHTML = `
                    <p><strong>Customer:</strong> ${data.customer}</p>
                    <p><strong>Date:</strong> ${data.date}</p>
                    <p><strong>Due Date:</strong> ${data.due_date}</p>
                    <p><strong>Status:</strong> ${data.status}</p>
                    <p><strong>Total Amount:</strong> ${data.total_amount}</p>
                    <h3>Items:</h3>
                    <ul>
                        ${data.items.map(item => `
                            <li>${item.product} - Quantity: ${item.quantity}, Price: ${item.unit_price}, Total: ${item.amount}</li>
                        `).join('')}
                    </ul>
                `;
                modal.style.display = 'block';
            });
    }

    function editInvoice(id) {
        // Similar to viewInvoice, but populate form for editing
        // Implement this functionality
    }

    function deleteInvoice(id) {
        if (confirm('Are you sure you want to delete this invoice?')) {
            fetch(`/invoices/${id}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();  // Refresh to remove deleted invoice
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }

    function generatePDF(id) {
        window.open(`/invoices/${id}/pdf`, '_blank');
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