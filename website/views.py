from flask import Blueprint, redirect, render_template, flash, session, url_for, request

views = Blueprint('views', __name__)

months_dict = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December',}

@views.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        flash("Please Log In First!!", 'error')
        return redirect(url_for('auth.login'))

@views.route('/settings', )
def settings():
    if 'user' in session:
        if session['is_admin'] == True:
            return render_template('settings/settings.html')
        else:
            flash("Sorry, contact admin. You don't have access to settings.", 'error')
            return redirect(url_for('views.home'))
    else:
        flash("Please Log In First!!", 'error')
        return redirect(url_for('auth.login'))
    

@views.route('/general-settings')
def general_settings():
    if 'user' in session:
        if session['is_admin'] == True:
            return render_template('settings/general-settings.html')
        else:
            flash("Sorry, contact admin. You don't have access to settings.", 'error')
            return redirect(url_for('views.home'))
        
    else:
        flash("Please Log In First!!", 'error')
        return redirect(url_for('auth.login'))

@views.route('/maintainance')
def maintaince():
    if 'user' in session:
        return render_template('widgets/maintainance.html')
    else:
        flash("Please Log In First!!", 'error')
        return redirect(url_for('auth.login'))

@views.route('/expenses')
def expenses():
    if 'user' in session:
        return render_template('widgets/expenses.html')
    else:
        flash("Please Log In First!!", 'error')
        return redirect(url_for('auth.login'))

@views.route('/summary', methods=['GET','POST'])
def summary_month():
    if 'user' in session:
        if request.method == 'GET':
            return render_template('widgets/summary.html')
        else:
            month = request.form.get('month')
            if month != '':
                month = month.split('-')
                session['summary'] = {'month':months_dict[month[1]], 'year':month[0]}
                return redirect(url_for('views.show_summary'))
            else:
                flash("Please choose the month!!", 'error')
                return render_template('widgets/summary.html')
    else:
        flash("Please Log In First!!", 'error')
        return redirect(url_for('auth.login'))
    
@views.route('/summary_show', methods=['GET','POST'])
def show_summary():
    if 'summary' in session:
        return render_template('widgets/summary_show.html')
    else:
        return redirect(url_for('views.summary_month'))