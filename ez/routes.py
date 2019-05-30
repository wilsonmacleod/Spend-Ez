from flask import render_template, url_for, flash, redirect
from ez import app, db
from ez.forms import LoginForm, Expend
from ez.models import User, Transactions

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = Expend()
    trans =Transactions.query.all()
    if form.validate_on_submit():
        trans = Transactions(amount=form.amount.data,note=form.note.data, cat=form.category.data)
        db.session.add(trans)
        db.session.commit()
        flash(f'Succesfully Submitted ${form.amount.data} Expense!', 'success')
        return redirect(url_for('home'))
    return render_template('index.html', trans = trans, form = form)