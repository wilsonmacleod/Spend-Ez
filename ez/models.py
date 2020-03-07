import datetime
from flask_login import UserMixin

from ez import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    trans = db.relationship('Transactions', backref='author', lazy=True) 
    trans_cats = db.relationship('TransCategories', backref='author', lazy=True) 
    month_budget = db.relationship('MonthlyBudgets', backref='author', lazy=True) 

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.password}', 'def:{self.budget}/month:{self.month_budget}')"

class TransCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"TransCategories('{self.id}', '{self.user_id}', '{self.name}')"

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    cat = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.date.today())

    def __repr__(self):
        return f"Transactions('{self.amount}', '{self.note}', '{self.cat}', '{self.date_posted}')"

class MonthlyBudgets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=500)
    month = db.Column(db.Integer, nullable=False, default=datetime.datetime.now().month)
    year = db.Column(db.Integer, nullable=False, default=datetime.datetime.now().year)

    def __repr__(self):
        return f"MonthlyBudgets('{self.user_id}', '{self.amount}', '{self.month}/{self.year}')"