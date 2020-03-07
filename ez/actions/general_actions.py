import datetime

from ez import db, login_manager
from ez.models import User, MonthlyBudgets

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class GeneralActions():

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

    def find_today(): ## mm, yy
        today = datetime.date.today()
        month_num = today.month
        return month_num, today.year

    def check_monthlybudget(user_id, month, year):
        check = MonthlyBudgets.query.filter_by(user_id=user_id).filter_by(month=month).filter_by(year=year).first()
        if check == None:
            def_budget = User.query.filter_by(id=user_id).first()
            return def_budget.budget, 'Default'
        month_string = GeneralActions.month_translate(month)
        return check.amount, f'{month_string} {year} specific'
    
    def update_default_budget(user, new_budget):
        user.budget = new_budget
        db.session.commit()
    
    def update_monthly_budget(user_id, new_budget, month_num, year):
        old = MonthlyBudgets.query.filter_by(user_id=user_id).filter_by(month=month_num).filter_by(year=year).first()
        if old != None:
            db.session.delete(old)
            db.session.commit()
        new_monthly = MonthlyBudgets(
                user_id=user_id, 
                amount=new_budget,
                month=month_num,
                year=year)
        db.session.add(new_monthly)
        db.session.commit()
