from flask import render_template, url_for, flash, redirect
from ez import app
from ez.forms import LoginForm, Expend
from ez.models import User, Transactions

trans = [
    {
        'amount': '94$', 
        'note': 'Gift for Haunani', 
        'cat': 'Romance',
        'date_posted': 'Feb 4, 2019'
    },
    {
        'amount': '20$', 
        'note': 'Treats for Daisy',
        'cat': 'Pets', 
        'date_posted': 'Feb 5, 2019'
    },
    {
        'amount': '26$', 
        'note': 'Donations',
        'cat': 'Other', 
        'date_posted': 'Feb 6, 2019'
    }
]

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = Expend()
    if form.validate_on_submit():
        flash(f'Succesfully Submitted ${form.amount.data} Expense!', 'success')
        return redirect(url_for('home'))
    return render_template('index.html', trans = trans, form = form)