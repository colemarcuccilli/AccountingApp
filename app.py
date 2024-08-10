from flask import Flask
from config import Config
from utils import format_currency

app = Flask(__name__)
app.config.from_object(Config)

# Register the format_currency filter
app.jinja_env.filters['format_currency'] = format_currency

from views import dashboard, chart_of_accounts, journal_entries, general_ledger, financial_statements, budgeting, forecasting, tax_reporting, audit_trail, custom_reports

app.register_blueprint(dashboard.bp)
app.register_blueprint(chart_of_accounts.bp)
app.register_blueprint(journal_entries.bp)
app.register_blueprint(general_ledger.bp)
app.register_blueprint(financial_statements.bp)
app.register_blueprint(budgeting.bp)
app.register_blueprint(forecasting.bp)
app.register_blueprint(tax_reporting.bp)
app.register_blueprint(audit_trail.bp)
app.register_blueprint(custom_reports.bp)

if __name__ == '__main__':
    app.run(debug=True)