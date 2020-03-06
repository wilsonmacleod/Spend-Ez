from ez import db, login_manager
from ez.models import User, TransCategories, Transactions
from ez.actions.general_actions import GeneralActions

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class TransactionActions():

    def change_category(user, old, new): #TransCategories
        old_cat = TransCategories.query.filter_by(user_id=user.id).filter_by(name=old).first()
        new_cat = TransCategories(id=old_cat.id, user_id=user.id, name=new)
        db.session.delete(old_cat)
        db.session.commit()
        db.session.add(new_cat)
        db.session.commit()

    def edit_trans(edit_transaction, user):
        trans_id = edit_transaction.trans_id.data
        old_trans = Transactions.query.filter_by(id=int(trans_id)).first()
        db.session.delete(old_trans)
        db.session.commit()

        new_trans = Transactions(
                            user_id=user.id, 
                            amount=edit_transaction.amount.data,
                            note=edit_transaction.note.data,
                            cat=edit_transaction.category.data,
                            date_posted=edit_transaction.date_posted.data
                        )
        db.session.add(new_trans)
        db.session.commit()

    def submit_trans(transaction_submit, user):
        trans = Transactions(
                            user_id=user.id, 
                            amount=transaction_submit.amount.data,
                            note=transaction_submit.note.data,
                            cat=transaction_submit.category.data,
                            date_posted=transaction_submit.date_posted.data
                            )
        db.session.add(trans)
        db.session.commit()

    def delete_trans(trans_id):
        trans = Transactions.query.get_or_404(trans_id)
        db.session.delete(trans)
        db.session.commit()
    
    def month_transactions(user, month_num, year): #Transactions
        trans = user.trans
        month_trans = []
        for each in trans:
            post = each.date_posted
            if post.month == month_num and post.year == year:
                month_trans.append(each)
        return month_trans

    def dict_hack(user):
        pull_user_cats = TransCategories.query.filter_by(user_id=user.id).all()
        cats = []
        for each in pull_user_cats:
            cats.append(each.name)
        return { key:0 for key in cats}  
    
    def list_cat_choices(user):
        inner_dict = TransactionActions.dict_hack(user)
        for key, value in inner_dict.items():
            inner_dict[key] = key
        return list(inner_dict.items())

    def ytd_transactions(user, year):
        trans = user.trans
        ytd = []
        sort_dict = TransactionActions.dict_hack(user)
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
            'January': TransactionActions.dict_hack(user),
            'February': TransactionActions.dict_hack(user),
            'March': TransactionActions.dict_hack(user),
            'April': TransactionActions.dict_hack(user),
            'May': TransactionActions.dict_hack(user),
            'June': TransactionActions.dict_hack(user),
            'July': TransactionActions.dict_hack(user),
            'August': TransactionActions.dict_hack(user),
            'September': TransactionActions.dict_hack(user),
            'October': TransactionActions.dict_hack(user),
            'November': TransactionActions.dict_hack(user),
            'December': TransactionActions.dict_hack(user),
        }
        for tran in trans:
            date = tran.date_posted
            if date.year == year:
                x = GeneralActions.month_translate(date.month)
                try:
                    t_dict[x][tran.cat] += tran.amount
                except KeyError: 
                    t_dict[x]["Other"] += tran.amount
                t_dict[x]['Total'] += tran.amount
        return t_dict
