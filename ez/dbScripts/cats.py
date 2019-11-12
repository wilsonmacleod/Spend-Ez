from ez import db
from ez import create_app
from ez.models import User, TransCategories, Transactions, General

app = create_app()

counter = 0
user_id = 1
default_cats = [
            'Food','Travel',
            'Entertainment', 'Education',
            'Transportation', 'Personal',
            'Health', 'Gift', 
            'Other', 'Total'
            ]

while user_id <= 5:
    for each in default_cats:
        with app.app_context():
            c = TransCategories(id=counter,user_id=int(user),name=each)
            db.session.add(c)
            db.session.commit()
            counter += 1
    user_id += 1
        

with app.app_context():
    display = TransCategories.query.all()
    print(f'TransCategories current state: \n{display}')
