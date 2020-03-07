import datetime
import random

from ez import db, login_manager
from ez.models import User, Transactions
from ez.actions.transaction_actions import TransactionActions
from ez.actions.general_actions import GeneralActions

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class DemoActions():

    def check_if_demo(user, mn, year): 
        trans = TransactionActions.month_transactions(user, mn, year)
        if len(trans) < 10:
            return True
        else:
            return False

    def random_dates(rando):
        mn, year = GeneralActions.find_today()
        date_list = []
        for each in range(0, len(rando)):
            day = 1
            try:
                day += random.randint(0, 31)
                date_list.append(datetime.date(year, mn, day))
            except ValueError:
                day = 1
                day += random.randint(0, 22)
                date_list.append(datetime.date(year, mn, day))
        return date_list

    def random_notes():
        notes = ["This is an automated note", 
                "No creativity Demo Note",
                "Is it harder to say or spell anemone?",
                "Please visit my creator's Github-https://github.com/wilsonmacleod",
                "I generated myself"
                    ]
        flip = random.randint(0, 11)
        if flip <= 3:
            note = notes[random.randint(0, 4)]
            return note
        else:
            return ""

    def create_demo_transactions(user):
        rando = [round((random.random())*100, 2)
                    for rando in range(1, random.randint(10, 20))]
        cats = [i for i in TransactionActions.dict_hack(user) if i != "Total"]
        date_list = DemoActions.random_dates(rando)
        index = 0
        for each in rando:
            trans = Transactions(user_id=user.id, amount=each,
                                    note=DemoActions.random_notes(),
                                    cat=cats[random.randint(0, len(cats)-1)],
                                    date_posted=date_list[index])
            index += 1
            db.session.add(trans)
            db.session.commit()