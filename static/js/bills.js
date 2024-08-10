// File: static/js/bills.js

document.addEventListener('DOMContentLoaded', function() {
    const newBillForm = document.getElementById('new-bill-form');
    const billsTable = document.getElementById('bills-table');
    const modal = document.getElementById('bill-modal');
    const vendorSelect = document.getElementById('vendor');
    const addItemButton = document.getElementById('add-item');

    vendorSelect.addEventListener('change', loadVendorTransactions);
    addItemButton.addEventListener('click', addBillItem);
    newBillForm.addEventListener('submit', createBill);
    billsTable.addEventListener('click', handleTableActions);

    function loadVendorTransactions() {
        const vendorId = vendorSelect.value;
        const itemsContainer = document.getElementById('bill-items');
        itemsContainer.innerHTML = '';
        
        if (vendorId) {
            fetch(`/vendor-transactions/${vendorId}`)
                .then(response => response.json())
                .then(transactions => {
                    transactions.forEach(transaction => {
                        addBillItem(transaction);
                    });
                });
        }
    }

    function addBillItem(transaction = null) {
        const itemsContainer = document.getElementById('bill-items');
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('bill-item');
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

    function createBill(e) {
        e.preventDefault();
        const formData = {
            vendor_id: vendorSelect.value,
            bill_date: document.getElementById('bill-date').value,
            due_date: document.getElementById('due-date').value,
            items: Array.from(document.querySelectorAll('.bill-item')).map(item => ({
                transaction_id: item.querySelector('.transaction-select').value,
                quantity: item.querySelector('.item-quantity').value
            }))
        };

        fetch('/bills', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Refresh to show new bill
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
                viewBill(id);
                break;
            case 'edit-btn':
                editBill(id);
                break;
            case 'delete-btn':
                deleteBill(id);
                break;
        }
    }

    function viewBill(id) {
        fetch(`/bills/${id}`)
            .then(response => response.json())
            .then(data => {
                const detailsDiv = document.getElementById('bill-details');
                detailsDiv.innerHTML = `
                    <p><strong>Vendor:</strong> ${data.vendor}</p>
                    <p><strong>Bill Date:</strong> ${data.bill_date}</p>
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

    function editBill(id) {
        // Implement edit functionality
    }

    function deleteBill(id) {
        if (confirm('Are you sure you want to delete this bill?')) {
            fetch(`/bills/${id}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();  // Refresh to remove deleted bill
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