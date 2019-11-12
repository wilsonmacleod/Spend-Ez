import datetime
import random
from flask_login import UserMixin

from ez import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=True)
    trans = db.relationship('Transactions', backref='author', lazy=True) 
    trans_cats = db.relationship('TransCategories', backref='author', lazy=True) 

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.password}, {self.budget})"

class TransCategories(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.user_id}', '{self.name}')"

    def change_category(user, old, new):
        old_cat = TransCategories.query.filter_by(user_id=user.id).filter_by(name=old).first()
        new_cat = TransCategories(id=old_cat.id, user_id=user.id, name=new)
        db.session.delete(old_cat)
        db.session.commit()
        db.session.add(new_cat)
        db.session.commit()


class Transactions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    cat = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.date.today())
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

    def dict_cheese(user):
        pull_user_cats = TransCategories.query.filter_by(user_id=user.id).all()
        cats = []
        for each in pull_user_cats:
            cats.append(each.name)
        return { key:0 for key in cats}  
    
    def form_cat_choices(user):
        inner_dict = Transactions.dict_cheese(user)
        for key, value in inner_dict.items():
            inner_dict[key] = key
        return list(inner_dict.items())

    def ytd_transactions(user, year):
        trans = user.trans
        ytd = []
        sort_dict = Transactions.dict_cheese(user)
        del sort_dict['Total']
        for each in trans:
            post = each.date_posted
            if post.year == year:
                ytd.append(each)
                try:
                    sort_dict[each.cat] += each.amount
                except KeyError: 
                    sort_dict["Other"] += each.amount
        max_cat = max(sort_dict.items(), key=lambda k: k[1])
        return round(sum([x.amount for x in ytd]), 2), max_cat

    def year_modal(user, year):
        trans = user.trans
        t_dict = {
            'January': Transactions.dict_cheese(user),
            'February': Transactions.dict_cheese(user),
            'March': Transactions.dict_cheese(user),
            'April': Transactions.dict_cheese(user),
            'May': Transactions.dict_cheese(user),
            'June': Transactions.dict_cheese(user),
            'July': Transactions.dict_cheese(user),
            'August': Transactions.dict_cheese(user),
            'September': Transactions.dict_cheese(user),
            'October': Transactions.dict_cheese(user),
            'November': Transactions.dict_cheese(user),
            'December': Transactions.dict_cheese(user),
        }
        for tran in trans:
            date = tran.date_posted
            x = General.month_translate(date.month)
            try:
                t_dict[x][tran.cat] += tran.amount
            except KeyError: 
                t_dict[x]["Other"] += tran.amount
            t_dict[x]['Total'] += tran.amount
        return t_dict

    def plot_gen(user, month_num, year):
        month_trans = Transactions.month_transactions(user, month_num, year)

        sort_dict = Transactions.dict_cheese(user)
        del sort_dict['Total']
        for trans in month_trans:
            try:
                sort_dict[str(trans.cat)] += trans.amount
            except:
                sort_dict["Other"] += trans.amount
        labels = [i for i in sort_dict]
        values = [i for x, i in sort_dict.items()]
        return labels, values

    def model_pie_gen(user, year):
        trans = user.trans
        ytd = []
        sort_dict = Transactions.dict_cheese(user)
        del sort_dict['Total']
        for each in trans:
            post = each.date_posted
            if post.year == year:
                ytd.append(each)
        for each in ytd:
            try:
                sort_dict[str(trans.cat)] += each.amount
            except:
                sort_dict["Other"] += each.amount
        labels = [i for x, i in sort_dict.items()]
        values = [i for i in sort_dict]
        colors = [
            "#C71585", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#F7464A"
        ]
        return labels, values, colors

    def pie_sub_data(labels, values):
        total = sum(labels)
        d = dict(zip(values, labels))
        for i, y in d.items():
            try:
                y = ((y/total)*100)
            except ZeroDivisionError:
                y = 0
            d[i] = round(y, 2)
        return d


class General():

    def find_today():
        today = datetime.date.today()
        month_num = today.month
        return month_num, today.year

    def month_translate(month_num):
        month_dict = {'1': 'January', '2': 'February',
                      '3': 'March', '4': 'April',
                      '5': 'May', '6': 'June',
                      '7': 'July',
                      '8': 'August', '9': 'September',
                      '10': 'October', '11': 'November',
                      '12': 'December'
                      }
        return month_dict[str(month_num)]

    def check(user, mn, year): 
        trans = Transactions.month_transactions(user, mn, year)
        if len(trans) < 10:
            return True
        else:
            return False

    def rando_dates(rando):
        mn, year = General.find_today()
        dplist = []
        for each in range(0, len(rando)):
            day = 1
            try:
                day += random.randint(0, 31)
                dplist.append(datetime.date(year, mn, day))
            except ValueError:
                day = 1
                day += random.randint(0, 22)
                dplist.append(datetime.date(year, mn, day))
        return dplist

    def rando_notes():
        notes = ["This is an automated note", 
                "No creativity Demo Note",
                    "Is it harder to say or spell anemone?",
                    "Please visit my creator's Github-https://github.com/wilsonmacleod",
                    "I generate myself, can YOU do that?"
                    ]
        flip = random.randint(0, 11)
        if flip <= 3:
            note = notes[random.randint(0, 4)]
            return note
        else:
            return ""

    def demo_transactions(user):
        rando = [round((random.random())*100, 2)
                    for rando in range(1, random.randint(10, 20))]
        cats = [i for i in Transactions.dict_cheese(user) if i != "Total"]
        dplist = General.rando_dates(rando)
        index = 0
        for each in rando:
            trans = Transactions(user_id=user.id, amount=each,
                                    note=General.rando_notes(),
                                    cat=cats[random.randint(0, 8)],
                                    date_posted=dplist[index])
            index += 1
            db.session.add(trans)
            db.session.commit()
