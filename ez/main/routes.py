from flask import render_template, url_for, flash, redirect, Blueprint, current_app
from flask_login import login_user, logout_user, current_user, login_required

from ez import db
from ez.main.forms import LoginForm, Expend, TimeTravel, UpdateBudget, EditTransaction, UpdateCategories
from ez.models import User, Transactions, General, TransCategories

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
    update_budget = UpdateBudget()  # Change your budget
    update_cats = UpdateCategories()

    categories = Transactions.form_cat_choices(user)
    categories = [x for x in categories if x != ("Total", "Total")]
    update_cats.category.choices = [x for x in categories if x != ("Other", "Other")]
    edit_transaction = EditTransaction() # Edit a Transaction
    edit_transaction.category.choices = categories
    transaction_submit = Expend()  # Submit a New Transaction
    transaction_submit.category.choices = categories

    if time_travel.validate_on_submit():
        if time_travel.years != None and time_travel.months != None:
            return redirect(url_for('main.landing',
                                    month_num=time_travel.months.data,
                                    year=time_travel.years.data))

    if update_budget.validate_on_submit():
        user.budget = update_budget.new_budget.data
        db.session.commit()
        return redirect(url_for('main.landing', month_num=month_num, year=year))
    
    if update_cats.validate_on_submit():
        new = update_cats.replacement.data.capitalize()
        if not any(new == item[0] for item in categories):
            TransCategories.change_category(user=user, 
                                            old=update_cats.category.data,
                                            new=new)
        else:
            pass
        return redirect(url_for('main.landing', month_num=month_num, year=year))
    
    if edit_transaction.validate_on_submit():  # Edit a Transaction

        try: #this is hacky to avoid this form when should be transaction_submit.validate_on_submit()
            trans_id = edit_transaction.trans_id.data
            old_trans = Transactions.query.filter_by(id=int(trans_id)).first()
            db.session.delete(old_trans)
            db.session.commit()

            new_trans = Transactions(user_id=user.id, amount=edit_transaction.amount.data,
                            note=edit_transaction.note.data,
                            cat=edit_transaction.category.data,
                            date_posted=edit_transaction.date_posted.data)
            db.session.add(new_trans)
            db.session.commit()
            flash(
                f'Succesfully Edited ${edit_transaction.amount.data} {edit_transaction.category.data} Expense!', 'info'
                )
            return redirect(url_for('main.landing', month_num=month_num, year=year))
        except ValueError:
            pass

    if transaction_submit.validate_on_submit():  # Submit a Transaction
        trans = Transactions(user_id=user.id, amount=transaction_submit.amount.data,
                             note=transaction_submit.note.data,
                             cat=transaction_submit.category.data,
                             date_posted=transaction_submit.date_posted.data)
        db.session.add(trans)
        db.session.commit()
        flash(
            f'Succesfully Submitted ${transaction_submit.amount.data} {transaction_submit.category.data} Expense!', 'success')
        return redirect(url_for('main.landing', month_num=month_num, year=year))

    return render_template('index.html',
                           time_travel=time_travel, transaction_submit=transaction_submit,
                           update_budget=update_budget, edit_transaction=edit_transaction,
                           update_cats=update_cats, modal_dict=modal_dict, month_num=month_num, 
                            month=General.month_translate(month_num),
                           year=year, trans=sort_trans, budget=budget, ytd_spend=round(ytd_spend,2),
                           max_cat=max_cat, total_spend=total_spend,
                           budget_percent=budget_percent,
                           max=int(round(budget*.40, -2)), labels=labels, values=values,
                           set=zip(pie_labels, pie_values, colors), modal_percs=modal_percs,
                           logged_in_user = user.username)

"""
DATA PASSING/UPDATING ROUTES
"""

@main.route("/spend-ez/landing/<int:trans_id>/delete<int:month_num>/<int:year>", methods=['GET', 'POST'])
@login_required
def delete_transaction(trans_id, month_num, year):
    trans = Transactions.query.get_or_404(trans_id)
    db.session.delete(trans)
    db.session.commit()
    flash('Your transaction has been deleted!', 'warning')
    return redirect(url_for('main.landing', month_num=month_num, year=year))

@main.route("/spend-ez/reload/", methods=['GET', 'POST'])
@login_required
def reload():
    month_num, year = General.find_today()
    return redirect(url_for('main.landing', month_num=month_num, year=year))
