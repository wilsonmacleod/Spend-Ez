from datetime import datetime
from ez import db

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable =  False)
    trans = db.relationship('Transactions', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Transactions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable = False)
    note = db.Column(db.Text, nullable=True)
    cat = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.amount}', '{self.note}', '{self.cat}', '{self.date_posted}')"
