from flask import Blueprint, render_template

bp = Blueprint('audit_trail', __name__, url_prefix='/audit-trail')

@bp.route('/')
def index():
    return render_template('audit_trail.html')