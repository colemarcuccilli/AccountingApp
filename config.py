import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    ACCOUNTS_FILE = os.path.join(basedir, 'data', 'accounts.csv')
    JOURNAL_ENTRIES_FILE = os.path.join(basedir, 'data', 'journal_entries.csv')