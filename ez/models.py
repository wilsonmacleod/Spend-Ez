import datetime
from ez import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable =  False)
    budget = db.Column(db.Integer, nullable = True)
    trans = db.relationship('Transactions', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.password}, {self.budget})"

class Transactions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable = False)
    cat = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.amount}', '{self.note}', '{self.cat}', '{self.date_posted}')"

    def month_transactions(user, month_num, year):
        
        trans = user.trans
    
        month_trans = []
        for each in trans:
            post = each.date_posted
            if post.month == month_num and post.year == year:
                month_trans.append(each)
        return month_trans

class General():

    def find_today():

        month_dict = {'1': 'January', '2': 'Feburary', '3': 'March', '4': 'April', 
                    '5': 'May', '6': 'June', '7': 'July',
                    '8': 'August', '9': 'September', 
                    '10': 'October', '11': 'November', '12': 'December'}

        today = datetime.date.today()
        month_num = today.month
        return month_dict[str(month_num)], month_num, today.year

