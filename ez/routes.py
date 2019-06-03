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
    month_num, year = General.find_today()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('landing', month_num=month_num, year=year))
        else:
            flash('Username or Password not correct. Login Unsuccessful.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

"""
DASHBOARD ROUTES
"""

@app.route('/landing/<int:month_num>/<int:year>/', methods = ['GET', 'POST'])
@login_required
def landing(month_num, year):
    
    user = User.query.filter_by(username=current_user.username).first() # Logged in user DB object/query
    trans = Transactions.month_transactions(user, month_num, year) #Transaction from this time for user
    
    ytd_spend, max_cat = Transactions.ytd_transactions(user, year) #YTD Metrics
    budget = user.budget #User stored budget
    total_spend = sum([x.amount for x in trans]) #User Transactions amounts
    budget_percent = (round((total_spend/budget)*100, 2))
    
    labels, values = Transactions.plot_gen(user, month_num, year) #Bar Plot Generator
    
    time_travel = TimeTravel() # Change view date/year
    transaction_submit = Expend() # Submit a New Transaction
    update_budget = UpdateBudget() # Change your budget

    if time_travel.validate_on_submit(): 
        if time_travel.years != '0' and time_travel.months != '0':
            return redirect(url_for('landing', month_num=time_travel.months.data, 
                                    year=time_travel.years.data))

    if update_budget.validate_on_submit():
        user.budget = update_budget.new_budget.data
        db.session.commit()
        return redirect(url_for('landing', month_num=month_num, year=year))
    if transaction_submit.validate_on_submit(): # Submit a Transaction
        trans = Transactions(user_id = user.id, amount=transaction_submit.amount.data, 
                            note=transaction_submit.note.data, 
                            cat=transaction_submit.category.data,
                            date_posted=transaction_submit.date_posted.data)
        db.session.add(trans)
        db.session.commit()
        flash(f'Succesfully Submitted ${transaction_submit.amount.data} Expense!', 'success')
        return redirect(url_for('landing', month_num=month_num, year=year))
    return render_template('index.html', 
                            time_travel = time_travel, transaction_submit = transaction_submit, 
                            update_budget = update_budget, 
                            month_num=month_num, month = General.month_translate(month_num), year = year, 
                            trans = list(reversed(trans)), budget = budget, ytd_spend = ytd_spend,
                            max_cat = max_cat, total_spend = total_spend, budget_percent = budget_percent, 
                            max=total_spend+100,labels=labels, values=values)

"""
DATA PASSING/UPDATING ROUTES
"""

@app.route("/landing/<int:trans_id>/delete<int:month_num>/<int:year>", methods = ['GET', 'POST'])
@login_required
def delete_transaction(trans_id, month_num, year):
    trans = Transactions.query.get_or_404(trans_id)
    db.session.delete(trans)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('landing', month_num=month_num, year=year))

@app.route("/reload/", methods = ['GET', 'POST'])
@login_required
def reload():
    month_num, year = General.find_today()
    return redirect(url_for('landing', month_num=month_num, year=year))