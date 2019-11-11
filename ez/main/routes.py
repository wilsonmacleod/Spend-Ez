from flask import render_template, url_for, flash, redirect, Blueprint, current_app
from flask_login import login_user, logout_user, current_user, login_required

from ez import db
from ez.main.forms import LoginForm, Expend, TimeTravel, UpdateBudget, EditTransaction
from ez.models import User, Transactions, General

main = Blueprint('main', __name__)

"""
'USER' ROUTES
"""

@main.route('/', methods=['GET', 'POST'])
@main.route('/spend-ez/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    month_num, year = General.find_today()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            if user.username == "ez_demo":
                if General.check(user, month_num, year):
                    flash('Dynamically Generated Transactions Succesful!', 'success')
                    General.demo_transactions(user)
            return redirect(url_for('main.landing', month_num=month_num, year=year))
        else:
            flash('Username or Password not correct. Login Unsuccessful.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/spend-ez/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

"""
DASHBOARD ROUTES
"""

@main.route('/spend-ez/landing/<int:month_num>/<int:year>/', methods=['GET', 'POST'])
@login_required
def landing(month_num, year):

    # Logged in user DB object/query
    user = User.query.filter_by(username=current_user.username).first()

    # Transaction from this time for user
    trans = Transactions.month_transactions(user, month_num, year)

    #METRICS
    sort_trans = reversed(
        sorted((t for t in trans), key=lambda x: x.date_posted))
    ytd_spend, max_cat = Transactions.ytd_transactions(
        user, year)  # YTD Metrics
    budget = user.budget  # User stored budget
    total_spend = round(sum([x.amount for x in trans]),
                        2)  # User Transactions amounts
    budget_percent = (round((total_spend/budget)*100, 2))
    modal_dict = Transactions.year_modal(user, year)

    #FIGURES
    labels, values = Transactions.plot_gen(
        user, month_num, year)  # Bar Plot Generator
    pie_labels, pie_values, colors = Transactions.model_pie_gen(
        user, year)  # Modal pie Generator
    modal_percs = Transactions.pie_sub_data(pie_labels, pie_values)

    #FORMS
    time_travel = TimeTravel()  # Change view date/year
    transaction_submit = Expend()  # Submit a New Transaction
    update_budget = UpdateBudget()  # Change your budget
    edit_transaction = EditTransaction()

    if time_travel.validate_on_submit():
        if time_travel.years != None and time_travel.months != None:
            return redirect(url_for('main.landing',
                                    month_num=time_travel.months.data,
                                    year=time_travel.years.data))

    if update_budget.validate_on_submit():
        user.budget = update_budget.new_budget.data
        db.session.commit()
        return redirect(url_for('main.landing', month_num=month_num, year=year))
    if transaction_submit.validate_on_submit():  # Submit a Transaction
        trans = Transactions(user_id=user.id, amount=transaction_submit.amount.data,
                             note=transaction_submit.note.data,
                             cat=transaction_submit.category.data,
                             date_posted=transaction_submit.date_posted.data)
        db.session.add(trans)
        db.session.commit()
        flash(
            f'Succesfully Submitted ${transaction_submit.amount.data} Expense!', 'success')
        return redirect(url_for('main.landing', month_num=month_num, year=year))
    return render_template('index.html',
                           time_travel=time_travel, transaction_submit=transaction_submit,
                           update_budget=update_budget, edit_transaction=edit_transaction,
                            modal_dict=modal_dict, month_num=month_num, 
                            month=General.month_translate(month_num),
                           year=year, trans=sort_trans, budget=budget, ytd_spend=round(ytd_spend,2),
                           max_cat=max_cat, total_spend=total_spend,
                           budget_percent=budget_percent,
                           max=int(round(budget*.40, -2)), labels=labels, values=values,
                           set=zip(pie_labels, pie_values, colors), modal_percs=modal_percs,
                           logged_in_user = user.username, 
                           )

"""
DATA PASSING/UPDATING ROUTES
"""

@main.route("/spend-ez/landing/<int:trans_id>/delete<int:month_num>/<int:year>", methods=['GET', 'POST'])
@login_required
def delete_transaction(trans_id, month_num, year):
    trans = Transactions.query.get_or_404(trans_id)
    db.session.delete(trans)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('main.landing', month_num=month_num, year=year))

@main.route("/spend-ez/landing/<int:trans_id>/edit<int:month_num>/<int:year>", methods=['GET', 'POST'])
@login_required
def edit_transaction(trans_id, month_num, year):
    return redirect(url_for('main.landing', month_num=month_num, year=year))

@main.route("/spend-ez/reload/", methods=['GET', 'POST'])
@login_required
def reload():
    month_num, year = General.find_today()
    return redirect(url_for('main.landing', month_num=month_num, year=year))
