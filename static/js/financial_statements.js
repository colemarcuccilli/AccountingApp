// File: static/js/financial_statements.js

document.addEventListener('DOMContentLoaded', function() {
    const statementType = document.getElementById('statement-type');
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    const generateBtn = document.getElementById('generate-statement');
    const statementContent = document.getElementById('statement-content');

    generateBtn.addEventListener('click', generateStatement);

    function generateStatement() {
        const type = statementType.value;
        const start = startDate.value;
        const end = endDate.value;

        let url;
        switch(type) {
            case 'income-statement':
                url = `/financial-statements/income-statement?start_date=${start}&end_date=${end}`;
                break;
            case 'balance-sheet':
                url = `/financial-statements/balance-sheet?as_of_date=${end}`;
                break;
            case 'cash-flow-statement':
                url = `/financial-statements/cash-flow-statement?start_date=${start}&end_date=${end}`;
                break;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                switch(type) {
                    case 'income-statement':
                        displayIncomeStatement(data);
                        break;
                    case 'balance-sheet':
                        displayBalanceSheet(data);
                        break;
                    case 'cash-flow-statement':
                        displayCashFlowStatement(data);
                        break;
                }
            });
    }

    function displayIncomeStatement(data) {
        statementContent.innerHTML = `
            <h2>Income Statement</h2>
            <h3>Revenue</h3>
            <ul>
                ${data.revenue.map(item => `<li>${item.account}: ${item.amount}</li>`).join('')}
            </ul>
            <p><strong>Total Revenue: ${data.total_revenue}</strong></p>
            <h3>Expenses</h3>
            <ul>
                ${data.expenses.map(item => `<li>${item.account}: ${item.amount}</li>`).join('')}
            </ul>
            <p><strong>Total Expenses: ${data.total_expenses}</strong></p>
            <p><strong>Net Income: ${data.net_income}</strong></p>
        `;
    }

    function displayBalanceSheet(data) {
        statementContent.innerHTML = `
            <h2>Balance Sheet</h2>
            <h3>Assets</h3>
            <ul>
                ${data.assets.map(item => `<li>${item.account}: ${item.amount}</li>`).join('')}
            </ul>
            <p><strong>Total Assets: ${data.total_assets}</strong></p>
            <h3>Liabilities</h3>
            <ul>
                ${data.liabilities.map(item => `<li>${item.account}: ${item.amount}</li>`).join('')}
            </ul>
            <p><strong>Total Liabilities: ${data.total_liabilities}</strong></p>
            <h3>Equity</h3>
            <ul>
                ${data.equity.map(item => `<li>${item.account}: ${item.amount}</li>`).join('')}
            </ul>
            <p><strong>Total Equity: ${data.total_equity}</strong></p>
        `;
    }

    function displayCashFlowStatement(data) {
        // Implement cash flow statement display logic here
    }
});