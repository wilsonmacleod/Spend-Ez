from ez import db, login_manager
from ez.models import User
from ez.actions.transaction_actions import TransactionActions


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RenderFigures():

    def main_plot_gen(user, month_num, year):
        month_trans = TransactionActions.month_transactions(user, month_num, year)

        sort_dict = TransactionActions.dict_hack(user)
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
        sort_dict = TransactionActions.dict_hack(user)
        del sort_dict['Total']
        for each in trans:
            post = each.date_posted
            if post.year == year:
                ytd.append(each)
        for each in ytd:
            try:
                sort_dict[str(each.cat)] += each.amount
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
