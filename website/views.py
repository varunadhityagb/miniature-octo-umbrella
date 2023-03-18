from flask import Blueprint, render_template, flash
from datetime import date
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    flash('Hello', 'info')
    return render_template('home.html', name="varun")

@views.route('/settings')
@login_required
def settings():
    return render_template('settings/settings.html')

@views.route('/water')
@login_required
def water():
    return render_template('settings/water.html')

@views.route('/maintainance')
@login_required
def maintaince():
    today = date.today()
    month = today.strftime("%B, %Y")
    return render_template('widgets/maintainance.html', month)

@views.route('/expenses')
@login_required
def expenses():
    return render_template('widgets/expenses.html')

@views.route('/summary')
def summary_month():
    flash("Hello World", 'error')
    return render_template('widgets/summary.html')