// File: static/js/accounts_payable.js

document.addEventListener('DOMContentLoaded', function() {
    const vendorFilter = document.getElementById('vendor-filter');
    const asOfDateFilter = document.getElementById('as-of-date');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const apTable = document.getElementById('ap-table');
    const agingTable = document.getElementById('aging-table');

    let agingChart, statusChart;

    applyFiltersBtn.addEventListener('click', loadAPData);

    function loadAPData() {
        const vendorId = vendorFilter.value;
        const asOfDate = asOfDateFilter.value;

        fetch(`/accounts-payable/data?vendor_id=${vendorId}&as_of_date=${asOfDate}`)
            .then(response => response.json())
            .then(data => {
                populateAPTable(data);
                updateCharts(data);
            });

        fetch('/accounts-payable/aging-summary')
            .then(response => response.json())
            .then(data => {
                populateAgingTable(data);
            });

        fetch('/accounts-payable/payment-efficiency')
            .then(response => response.json())
            .then(data => {
                updatePaymentEfficiency(data);
            });
    }

    function populateAPTable(data) {
        const tbody = apTable.querySelector('tbody');
        tbody.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.bill_id}</td>
                <td>${row.vendor_name}</td>
                <td>${row.bill_date}</td>
                <td>${row.due_date}</td>
                <td>${row.total_amount}</td>
                <td>${row.remaining}</td>
                <td>${row.days_overdue}</td>
                <td>${row.status}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function populateAgingTable(data) {
        const tbody = agingTable.querySelector('tbody');
        tbody.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.vendor_name}</td>
                <td>${row.current}</td>
                <td>${row['1-30_days']}</td>
                <td>${row['31-60_days']}</td>
                <td>${row['60+_days']}</td>
                <td>${row.total}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function updateCharts(data) {
        const agingData = {
            current: 0,
            '1-30_days': 0,
            '31-60_days': 0,
            '60+_days': 0
        };

        const statusData = {
            'Current': 0,
            'Slightly Overdue': 0,
            'Overdue': 0,
            'Very Overdue': 0,
            'Severely Overdue': 0
        };

        data.forEach(row => {
            const amount = parseFloat(row.remaining.replace(/[^0-9.-]+/g,""));
            if (row.days_overdue <= 0) agingData.current += amount;
            else if (row.days_overdue <= 30) agingData['1-30_days'] += amount;
            else if (row.days_overdue <= 60) agingData['31-60_days'] += amount;
            else agingData['60+_days'] += amount;

            statusData[row.status] += amount;
        });

        updateAgingChart(agingData);
        updateStatusChart(statusData);
    }

    function updateAgingChart(data) {
        const ctx = document.getElementById('aging-chart').getContext('2d');
        if (agingChart) agingChart.destroy();
        agingChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Current', '1-30 Days', '31-60 Days', '60+ Days'],
                datasets: [{
                    data: Object.values(data),
                    backgroundColor: ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'AP Aging'
                }
            }
        });
    }

    function updateStatusChart(data) {
        const ctx = document.getElementById('status-chart').getContext('2d');
        if (statusChart) statusChart.destroy();
        statusChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Amount',
                    data: Object.values(data),
                    backgroundColor: '#2196F3'
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'AP by Status'
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    function updatePaymentEfficiency(data) {
        const efficiencyDiv = document.getElementById('payment-efficiency');
        efficiencyDiv.innerHTML = `
            <h3>Payment Efficiency (Last 90 Days)</h3>
            <p>Total Billed: ${data.total_billed}</p>
            <p>Total Paid: ${data.total_paid}</p>
            <p>Efficiency: ${data.efficiency}</p>
        `;
    }

    // Initial load
    loadAPData();
});