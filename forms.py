# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class AccountForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired(), Length(max=100)])
    type = SelectField('Account Type', choices=[('asset', 'Asset'), ('liability', 'Liability'), ('equity', 'Equity'), ('revenue', 'Revenue'), ('expense', 'Expense')])
    submit = SubmitField('Submit')

class JournalEntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    debit_account = SelectField('Debit Account', coerce=int)
    credit_account = SelectField('Credit Account', coerce=int)
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Submit')

class BudgetForm(FlaskForm):
    account = SelectField('Account', coerce=int)
    year = SelectField('Year', coerce=int)
    month = SelectField('Month', coerce=int, choices=[(i, i) for i in range(1, 13)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class ForecastForm(FlaskForm):
    account = SelectField('Account', coerce=int)
    date = DateField('Date', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class TaxReportForm(FlaskForm):
    report_type = SelectField('Report Type', choices=[('income', 'Income Tax'), ('sales', 'Sales Tax'), ('payroll', 'Payroll Tax')])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Generate Report')

class CustomReportForm(FlaskForm):
    name = StringField('Report Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    query = TextAreaField('SQL Query', validators=[DataRequired()])
    submit = SubmitField('Save Report')