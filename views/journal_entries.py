from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_journal_entries, add_journal_entry, get_accounts, format_currency
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('journal_entries', __name__, url_prefix='/journal-entries')

@bp.route('/')
def index():
    entries = get_journal_entries()
    logger.debug(f"Entries received in view: {entries}")
    formatted_entries = []
    for entry in entries:
        try:
            amount = float(entry['amount'])
            formatted_entry = entry.copy()
            formatted_entry['amount'] = format_currency(amount)
            formatted_entries.append(formatted_entry)
            logger.debug(f"Formatted entry: {formatted_entry}")
        except ValueError as e:
            logger.error(f"Error formatting amount for entry {entry.get('id', 'unknown')}: {str(e)}")
            flash(f"Error displaying entry {entry.get('id', 'unknown')}", 'error')
    return render_template('journal_entries.html', entries=formatted_entries)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            date = request.form['date']
            description = request.form['description']
            debit_account_id = request.form['debit_account_id']
            credit_account_id = request.form['credit_account_id']
            amount = request.form['amount']
            
            if float(amount) <= 0:
                raise ValueError("Amount must be positive")
            
            add_journal_entry(date, description, debit_account_id, credit_account_id, amount)
            flash('Journal entry added successfully', 'success')
            return redirect(url_for('journal_entries.index'))
        except ValueError as e:
            flash(str(e), 'error')
            logger.warning(f"Invalid input for journal entry: {str(e)}")
        except Exception as e:
            flash('An error occurred while adding the journal entry', 'error')
            logger.error(f"Error adding journal entry: {str(e)}")
    
    accounts = get_accounts()
    return render_template('journal_entry_form.html', accounts=accounts)