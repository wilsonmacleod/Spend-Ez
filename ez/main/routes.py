from flask import render_template, url_for, flash, redirect, Blueprint, current_app
from flask_login import login_user, logout_user, current_user, login_required

from ez import db
from ez.main.forms import LoginForm, Expend, TimeTravel, UpdateBudget, EditTransaction, UpdateCategories
from ez.models import User, Transactions
from ez.actions.demo_actions import DemoActions
from ez.actions.general_actions import GeneralActions
from ez.actions.render_figure_actions import RenderFigures
from ez.actions.transaction_actions import TransactionActions

main = Blueprint('main', __name__)

"""
'USER' ROUTES
"""

@main.route('/', methods=['GET', 'POST'])
@main.route('/spend-ez/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    month_num, year = GeneralActions.find_today()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.password == login_form.password.data:
            login_user(user)
            if user.username == "ez_demo":
                if DemoActions.check_if_demo(user, month_num, year):
                    flash('Dynamically Generated Transactions Succesful!', 'success')
                    DemoActions.create_demo_transactions(user)
            return redirect(url_for('main.landing', month_num=month_num, year=year))
        else:
            flash('Username or Password not correct. Login Unsuccessful.', 'danger')
    return render_template('login.html', title='Login', form=login_form)

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
    
    # DETAILS
    month_string = GeneralActions.month_translate(month_num)
    budget, budget_type = GeneralActions.check_monthlybudget(user.id, month_num, year)
    trans = TransactionActions.month_transactions(user, month_num, year)
    sort_trans = reversed(sorted((t for t in trans), key=lambda x: x.date_posted))

    #METRICS
    ytd_spend, max_cat = TransactionActions.ytd_transactions(user, year)  # YTD Metrics
    total_spend = round(sum([x.amount for x in trans]), 2)  # User Transactions amounts
    budget_percent = (round((total_spend/budget)*100, 2))
    modal_dict = TransactionActions.year_modal_spend(user, year)
    modal_budget_dict = TransactionActions.year_modal_budget(user.id, year)
    
    #FIGURES
    labels, values = RenderFigures.main_plot_gen(user, month_num, year)  # Bar Plot Generator
    pie_labels, pie_values, colors = RenderFigures.model_pie_gen(user, year)  # Modal pie Generator
    modal_percs = RenderFigures.pie_sub_data(pie_labels, pie_values)

    #FORMS
    time_travel = TimeTravel()  # Change view date/year
    update_budget = UpdateBudget()  # Change your budget
    update_budget.options.choices.append(('Monthly', month_string))
    update_categories = UpdateCategories()

    categories = TransactionActions.list_cat_choices(user)
    categories = [x for x in categories if x != ("Total", "Total")]
    update_categories.category.choices = [x for x in categories if x != ("Other", "Other")]

    edit_transaction = EditTransaction() # Edit a Transaction
    edit_transaction.category.choices = categories
    transaction_submit = Expend()  # Submit a New Transaction
    transaction_submit.category.choices = categories

    #FORM ACTION HANDLERS
    if update_categories.validate_on_submit():
        new = update_categories.replacement.data.capitalize()
        if not any(new == item[0] for item in categories):
            TransactionActions.change_category(user=user, old=update_categories.category.data, new=new)
        return redirect(url_for('main.landing', month_num=month_num, year=year))

    if time_travel.validate_on_submit():
        if time_travel.years != None and time_travel.months != None:
            return redirect(url_for('main.landing', month_num=time_travel.months.data, year=time_travel.years.data))

    if update_budget.validate_on_submit():
        new_budget = update_budget.new_budget.data
        if update_budget.options.data == 'Default':
            GeneralActions.update_default_budget(user, new_budget)
        else:
            GeneralActions.update_monthly_budget(user.id, new_budget, month_num, year)
        flash(f'Succesfully edited {update_budget.options.data} budget to ${int(update_budget.new_budget.data)}', 'info')
        return redirect(url_for('main.landing', month_num=month_num, year=year))
    
    if edit_transaction.validate_on_submit():  # Edit a Transaction
        try:
            TransactionActions.edit_trans(edit_transaction, user)
            flash(f'Succesfully edited ${edit_transaction.amount.data} {edit_transaction.category.data} expense!', 'info')
            return redirect(url_for('main.landing', month_num=month_num, year=year))
        except:
            """value error"""
            pass

    if transaction_submit.validate_on_submit():  # Submit a Transaction
        TransactionActions.submit_trans(transaction_submit, user)
        flash(f'Succesfully submitted ${transaction_submit.amount.data} {transaction_submit.category.data} expense!', 'success')
        return redirect(url_for('main.landing', month_num=month_num, year=year))

    return render_template(
                        'index.html',
                        logged_in_user = user.username, # current username
                        month_num=month_num, 
                        month=month_string,
                        budget_type=budget_type,
                        #FORMS
                        time_travel=time_travel,  
                        transaction_submit=transaction_submit,
                        update_budget=update_budget, 
                        edit_transaction=edit_transaction,
                        update_cats=update_categories, 
                        #METRICS
                        modal_dict=modal_dict, 
                        modal_budget_dict=modal_budget_dict,
                        year=year, 
                        trans=sort_trans, 
                        budget=budget, 
                        ytd_spend=round(ytd_spend,2),
                        max_cat=max_cat, 
                        total_spend=total_spend,
                        budget_percent=budget_percent,
                        #FIGURES
                        max=int(round(budget*.40, -2)), 
                        labels=labels,
                        values=values,
                        set=zip(pie_labels, pie_values, colors), 
                        modal_percs=modal_percs
                        )

"""
DATA PASSING/UPDATING ROUTES
"""

@main.route("/spend-ez/landing/<int:trans_id>/delete<int:month_num>/<int:year>", methods=['GET', 'POST'])
@login_required
def delete_transaction(trans_id, month_num, year):
    TransactionActions.delete_trans(trans_id)
    flash('Your transaction has been deleted!', 'warning')
    return redirect(url_for('main.landing', month_num=month_num, year=year))

@main.route("/spend-ez/reload/", methods=['GET', 'POST'])
@login_required
def reload():
    month_num, year = GeneralActions.find_today()
    return redirect(url_for('main.landing', month_num=month_num, year=year))
