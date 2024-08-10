from flask import Blueprint, render_template, request, jsonify
from utils import get_accounts, get_journal_entries, get_budget, format_currency
from datetime import datetime, timedelta
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

bp = Blueprint('forecasting', __name__, url_prefix='/forecasting')

@bp.route('/')
def index():
    accounts = get_accounts()
    return render_template('forecasting.html', accounts=accounts)

@bp.route('/generate', methods=['POST'])
def generate_forecast():
    account_id = request.form['account_id']
    periods = int(request.form['periods'])
    
    # Get historical data
    entries = get_journal_entries()
    account_entries = [entry for entry in entries if entry['debit_account_id'] == account_id or entry['credit_account_id'] == account_id]
    
    # Prepare data for forecasting
    df = pd.DataFrame(account_entries)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['amount'] = df['amount'].astype(float)
    
    # Aggregate by month
    monthly_data = df.resample('M')['amount'].sum()
    
    # Perform forecasting using ARIMA
    model = ARIMA(monthly_data, order=(1,1,1))
    results = model.fit()
    forecast = results.forecast(steps=periods)
    
    # Prepare forecast data for display
    forecast_data = [
        {
            'date': date.strftime('%Y-%m-%d'),
            'amount': format_currency(amount)
        }
        for date, amount in zip(forecast.index, forecast.values)
    ]
    
    return jsonify(forecast_data)