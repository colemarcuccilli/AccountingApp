// File: static/js/general_ledger.js

document.addEventListener('DOMContentLoaded', function() {
    const accountFilter = document.getElementById('account-filter');
    const startDateFilter = document.getElementById('start-date');
    const endDateFilter = document.getElementById('end-date');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const ledgerTable = document.getElementById('ledger-table');
    const trialBalanceTable = document.getElementById('trial-balance-table');

    applyFiltersBtn.addEventListener('click', loadLedgerData);

    function loadLedgerData() {
        const accountId = accountFilter.value;
        const startDate = startDateFilter.value;
        const endDate = endDateFilter.value;

        fetch(`/general-ledger/data?account_id=${accountId}&start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {
                populateLedgerTable(data);
            });

        fetch('/general-ledger/trial-balance')
            .then(response => response.json())
            .then(data => {
                populateTrialBalanceTable(data);
            });
    }

    function populateLedgerTable(data) {
        const tbody = ledgerTable.querySelector('tbody');
        tbody.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.date}</td>
                <td>${row.description}</td>
                <td>${row.debit}</td>
                <td>${row.credit}</td>
                <td>${row.balance}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function populateTrialBalanceTable(data) {
        const tbody = trialBalanceTable.querySelector('tbody');
        tbody.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.account_name}</td>
                <td>${row.debit}</td>
                <td>${row.credit}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Initial load
    loadLedgerData();
});