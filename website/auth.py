from flask import Blueprint, redirect, render_template, request, flash, session, url_for
import MySQLdb.cursors
from . import mysql, get_auth_key
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select email, user_password, id, full_name, admin_access from users;')
        data = cur.fetchall()
        email = request.form.get('email')
        password = request.form.get('password')
        keep_logged_in = request.form.get('keeplogCheck')
        

        emails = []
        passwords = []
        ids = []
        full_names = []
        admins = []

        for i in data:
            emails.append(i['email'])
            passwords.append(i['user_password'])
            ids.append(i['id'])
            full_names.append(i['full_name'])
            admins.append(i['admin_access'])

        try:
            required_index = emails.index(email)
            id_queried = ids[required_index]
            name_queried = full_names[required_index]
            password_queried = passwords[required_index]
            admin_access = admins[required_index]

            if check_password_hash(password_queried, password):
                if keep_logged_in == None:
                    pass
                elif keep_logged_in == 'on':
                    session.permanent = True
                    
                session['user'] = id_queried
                session['name'] = name_queried
                session['email'] = email
                if admin_access == 1:
                    session['is_admin'] = True
                else:
                    session['is_admin'] = False
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password Entered!!", 'error')
        except:
            flash("Check the email entered or Sign Up", 'error')
            

        return render_template('login.html')
    else:
        if 'user' in session:
            return redirect(url_for('views.home'))
        else:
            return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        email = request.form.get('email')
        name = request.form.get('name')
        dob = request.form.get('dateob')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        auth_key = get_auth_key(dob)
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT email FROM users;')
        emails_querried = cur.fetchall()
        emails = []
        for i in emails_querried:
            emails.append(i['email'])
        print(emails)
        if email in emails:
            flash("Email already used!!", 'error')
        elif (('@') or ('.com') or ('.edu')) not in email:
            flash("Email not valid!!", 'error')
        elif len(name) < 2: 
            flash("Name too short!!", 'error')
        elif len(password) < 8:
            flash("Password too short", 'error')
        elif password != repassword:
            flash("Passwords don't match!!", 'error')
        else:
            password = generate_password_hash(password, method="sha256")
            if emails == []:
                cur.execute(f"INSERT INTO users (full_name,email,auth_key,user_password, admin_access) VALUES ('{name}','{email}','{auth_key}','{password}', '1');")
                session['is_admin'] = True
            else:
                cur.execute(f"INSERT INTO users (full_name,email,auth_key,user_password, admin_access) VALUES ('{name}','{email}','{auth_key}','{password}', '0');")
            mysql.connection.commit()

            cur.execute(f"SELECT id FROM users WHERE email='{email}'")
            id = cur.fetchone()
            session['user'] = id
            session['name'] = name
            session['email'] = email
            return redirect(url_for('views.home'))
        
        return render_template('signup.html')
    else:
        if 'user' in session:
            return redirect(url_for('views.home'))
        else:
            return render_template('signup.html')
        

@auth.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('name', None)
        session.pop('email', None)
        session.pop('summary', None)
        return redirect(url_for('auth.login'))
