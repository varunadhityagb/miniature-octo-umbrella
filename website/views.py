from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', name="varun")

@views.route('/settings')
def settings():
    return render_template('settings.html')

@views.route('/water')
def water():
    return render_template('water.html')