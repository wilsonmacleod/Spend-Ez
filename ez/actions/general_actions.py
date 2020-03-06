import datetime

from ez import db, login_manager

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
