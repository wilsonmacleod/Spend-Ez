from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Length, Email
from datetime import datetime

from ez.models import Transactions

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class Expend(FlaskForm):

    amount = FloatField(validators=[DataRequired()])
    category = RadioField(u'category', validators=[DataRequired()], 
                            choices = [], coerce=str, default = 'Category')
    date_posted = DateField(default=datetime.today)
    note = StringField()
    submit = SubmitField('Submit')

class EditTransaction(FlaskForm):
    amount = FloatField(validators=[DataRequired()])
    category = SelectField(u'category', validators=[DataRequired()], 
                            choices = [], coerce=str)
    date_posted = DateField()
    note = StringField()
    et_submit = SubmitField('Submit')
    trans_id = StringField()

class TimeTravel(FlaskForm):

    month_choices = [(None, 'Month'), ('1', 'January'), ('2', 'February'), ('3', 'March'), 
                ('4', 'April'), ('5', 'May'), ('6', 'June'), 
                ('7', 'July'), ('8', 'August'), 
                ('9', 'September'), ('10', 'October'), 
                ('11', 'November'), ('12', 'December')]
    year_choices = [(None, 'Year'), ('2019', '2019'), ('2020', '2020'), 
                ('2021', '2021'), ('2022', '2022'), 
                ('2023', '2023'), ('2024', '2024'),
                ('2025', '2025'), ('2026', '2026')] 
    months = SelectField(u'2019', validators=[DataRequired()], 
                            choices = month_choices, coerce=str, default="Month")
    years = SelectField(u'2020', validators=[DataRequired()], 
                            choices = year_choices, coerce=str, default=datetime.today().year)
    submit = SubmitField('Go')

class UpdateBudget(FlaskForm):
    new_budget = FloatField(validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateCategories(FlaskForm):
    category = SelectField(u'category', validators=[DataRequired()], 
                            choices = [], coerce=str, default="Old Category")
    replacement = StringField(validators=[DataRequired()])
    submit = SubmitField('Update')