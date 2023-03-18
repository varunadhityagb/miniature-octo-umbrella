from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,password)
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')