from flask import render_template, url_for, flash, redirect
from ez import app, db
from ez.forms import LoginForm, Expend, YearMonth
from ez.models import User, Transactions, General
from flask_login import login_user, logout_user, current_user, login_required

import datetime

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/landing', methods = ['GET', 'POST'])
@login_required
def landing():

    time_travel = YearMonth() # Forms
    transaction_submit = Expend()

    month, month_num, year = General.find_today() #Today's str, int date and year
    user = User.query.filter_by(username=current_user.username).first() #Logged in user
    trans = Transactions.month_transactions(user, month_num, year) #Transaction from this month for user
    budget = user.budget #User stored budget
    total_spend = sum([x.amount for x in trans]) #User Transactions amounts
    budget_percent = (round((total_spend/budget)*100, 2))
    
    if transaction_submit.validate_on_submit(): # Submit a Transaction
        trans = Transactions(user_id = user.id, amount=transaction_submit.amount.data, 
                            note=transaction_submit.note.data, 
                            cat=transaction_submit.category.data)
        db.session.add(trans)
        db.session.commit()
        flash(f'Succesfully Submitted ${transaction_submit.amount.data} Expense!', 'success')
        return redirect(url_for('landing'))
    return render_template('index.html', time_travel = time_travel, 
                            transaction_submit = transaction_submit, 
                            month = month, year = year, trans = list(reversed(trans)), budget = budget, 
                            total_spend = total_spend,
                            budget_percent = budget_percent)

@app.route("/landing/<int:trans_id>/delete", methods=['POST'])
@login_required
def delete_transaction(trans_id):
    trans = Transactions.query.get_or_404(trans_id)
    db.session.delete(trans)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('landing'))