from flask import Blueprint, render_template

bp = Blueprint('custom_reports', __name__, url_prefix='/custom-reports')

@bp.route('/')
def index():
    return render_template('custom_reports.html')