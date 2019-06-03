from flask import render_template, url_for, flash, redirect
from ez import app, db
from ez.forms import LoginForm, Expend, TimeTravel, UpdateBudget
from ez.models import User, Transactions, General
from flask_login import login_user, logout_user, current_user, login_required

"""
'USER' ROUTES
"""

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('landing'))
        else:
            flash('Username or Password not correct. Login Unsuccessful.', 'danger')
    return render_template('login.html', title='Login', form=form)

"""
DASHBOARD ROUTES
"""

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/landing', methods = ['GET', 'POST'])
@login_required
def landing():

    time_travel = TimeTravel() # Forms
    transaction_submit = Expend()
    ub = UpdateBudget()

    month, month_num, year = General.find_today() #Today's str, int date and year
    user = User.query.filter_by(username=current_user.username).first() #Logged in user
    trans = Transactions.month_transactions(user, month_num, year) #Transaction from this month for user
    ytd_spend, max_cat = Transactions.ytd_transactions(user, year)

    budget = user.budget #User stored budget
    total_spend = sum([x.amount for x in trans]) #User Transactions amounts
    budget_percent = (round((total_spend/budget)*100, 2))
    labels, values = Transactions.plot_gen(user, month_num, year)
    
    if time_travel.validate_on_submit():
        if time_travel.years != '0' and time_travel.months != '0':
            return redirect(url_for('tt_landing', month_num=time_travel.months.data, year=time_travel.years.data))
    if ub.validate_on_submit():
        user.budget = ub.new_budget.data
        db.session.commit()
        return redirect(url_for('landing'))
    if transaction_submit.validate_on_submit(): # Submit a Transaction
        trans = Transactions(user_id = user.id, amount=transaction_submit.amount.data, 
                            note=transaction_submit.note.data, 
                            cat=transaction_submit.category.data,
                            date_posted=transaction_submit.date_posted.data)
        db.session.add(trans)
        db.session.commit()
        flash(f'Succesfully Submitted ${transaction_submit.amount.data} Expense!', 'success')
        return redirect(url_for('landing'))
    return render_template('index.html', time_travel = time_travel, 
                            transaction_submit = transaction_submit, ub = ub,
                            month = month, year = year, trans = list(reversed(trans)), budget = budget, 
                            ytd_spend = ytd_spend, max_cat = max_cat, total_spend = total_spend,
                            budget_percent = budget_percent, max=total_spend+50, 
                            labels=labels, values=values)

@app.route('/landing/<int:month_num>/<int:year>/time-travel', methods = ['GET', 'POST'])
@login_required
def tt_landing(month_num, year):

    time_travel = TimeTravel() # Forms
    transaction_submit = Expend()
    ub = UpdateBudget()
    
    try:
        month = General.month_translate(month_num)
    except KeyError:
        return redirect(url_for('landing'))
    user = User.query.filter_by(username=current_user.username).first() #Logged in user
    trans = Transactions.month_transactions(user, month_num, year) #Transaction from this month for user
    ytd_spend, max_cat = Transactions.ytd_transactions(user, year)

    budget = user.budget #User stored budget
    total_spend = sum([x.amount for x in trans]) #User Transactions amounts
    budget_percent = (round((total_spend/budget)*100, 2))
    labels, values = Transactions.plot_gen(user, month_num, year)

    if time_travel.validate_on_submit():
        if time_travel.years != '0' and time_travel.months != '0':
            return redirect(url_for('tt_landing', month_num=time_travel.months.data, year=time_travel.years.data))

    if ub.validate_on_submit():
        user.budget = ub.new_budget.data
        db.session.commit()
        return redirect(url_for('landing'))
    if transaction_submit.validate_on_submit(): # Submit a Transaction
        trans = Transactions(user_id = user.id, amount=transaction_submit.amount.data, 
                            note=transaction_submit.note.data, 
                            cat=transaction_submit.category.data,
                            date_posted=transaction_submit.date_posted.data)
        db.session.add(trans)
        db.session.commit()
        flash(f'Succesfully Submitted ${transaction_submit.amount.data} Expense!', 'success')
        return redirect(url_for('landing'))
    return render_template('index.html', time_travel = time_travel, 
                            transaction_submit = transaction_submit, ub = ub,
                            month = month, year = year, trans = list(reversed(trans)), budget = budget, 
                            ytd_spend = ytd_spend, max_cat = max_cat, total_spend = total_spend,
                            budget_percent = budget_percent, max=total_spend+50, 
                            labels=labels, values=values)

"""
DATA PASSING/UPDATING ROUTES
"""

@app.route("/landing/<int:trans_id>/delete", methods=['POST'])
@login_required
def delete_transaction(trans_id):
    trans = Transactions.query.get_or_404(trans_id)
    db.session.delete(trans)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('landing'))