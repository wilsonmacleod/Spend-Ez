import datetime
from ez import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=True)
    trans = db.relationship('Transactions', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.password}, {self.budget})"


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

    def dict_cheese():  # hacky way to instance empty "template" dict
        inner_dict = {
            'Food': 0, 'Travel': 0,
            'Entertainment': 0, 'Education': 0,
            'Transportation': 0, 'Personal': 0,
            'Health': 0, 'Gift': 0, 'Other': 0,
            'Total': 0
        }
        return inner_dict

    def ytd_transactions(user, year):
        trans = user.trans
        ytd = []
        sort_dict = Transactions.dict_cheese()
        del sort_dict['Total']
        for each in trans:
            post = each.date_posted
            if post.year == year:
                ytd.append(each)
                sort_dict[each.cat] += int(each.amount)
        max_cat = max(sort_dict.items(), key=lambda k: k[1])
        return round(sum([x.amount for x in ytd]), 2), max_cat

    def year_modal(user, year):
        trans = user.trans
        t_dict = {
            'January': Transactions.dict_cheese(),
            'February': Transactions.dict_cheese(),
            'March': Transactions.dict_cheese(),
            'April': Transactions.dict_cheese(),
            'May': Transactions.dict_cheese(),
            'June': Transactions.dict_cheese(),
            'July': Transactions.dict_cheese(),
            'August': Transactions.dict_cheese(),
            'September': Transactions.dict_cheese(),
            'October': Transactions.dict_cheese(),
            'November': Transactions.dict_cheese(),
            'December': Transactions.dict_cheese(),
        }
        for tran in trans:
            date = tran.date_posted
            x = General.month_translate(date.month)
            t_dict[x][tran.cat] += round(tran.amount,2)
            t_dict[x]['Total'] += round(tran.amount,2)
        return t_dict

    def plot_gen(user, month_num, year):
        month_trans = Transactions.month_transactions(user, month_num, year)

        sort_dict = Transactions.dict_cheese()
        del sort_dict['Total']
        for trans in month_trans:
            sort_dict[str(trans.cat)] += trans.amount
        labels = [i for i in sort_dict]
        values = [i for x, i in sort_dict.items()]
        return labels, values

    def model_pie_gen(user, year):
        trans = user.trans
        ytd = []
        sort_dict = Transactions.dict_cheese()
        del sort_dict['Total']
        for each in trans:
            post = each.date_posted
            if post.year == year:
                ytd.append(each)
        for each in ytd:
            sort_dict[str(each.cat)] += int(each.amount)
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
        month_dict = {'1': 'January', '2': 'Feburary', '3': 'March', '4': 'April',
                      '5': 'May', '6': 'June', '7': 'July',
                      '8': 'August', '9': 'September',
                      '10': 'October', '11': 'November', '12': 'December'}
        return month_dict[str(month_num)]
