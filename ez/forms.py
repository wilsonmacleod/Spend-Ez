from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class Expend(FlaskForm):
    amount = FloatField(validators=[DataRequired()])
    category_choices = [('Food', 'Food'), ('Travel', 'Travel'), 
                        ('Entertainment', 'Entertainment'), ('Education', 'Education'), 
                        ('Transportation', 'Transportation'), 
                        ('Personal', 'Personal'), ('Health', 'Health'), 
                        ('Gift', 'Gift'), ('Other', 'Other')]
    category = SelectField(u'category', validators=[DataRequired()], 
                            choices = category_choices, coerce=str, default = 'Category')
    note = TextAreaField()
    submit = SubmitField('Submit Expense')

class YearMonth(FlaskForm):
    
    def choice_gen(year):

        months = [('1', 'January'), ('2', 'February'), ('3', 'March'), 
                    ('4', 'April'), ('5', 'May'), ('6', 'June'), 
                    ('7', 'July'), ('8', 'August'), 
                    ('9', 'September'), ('10', 'October'), 
                    ('11', 'November'), ('12', 'December')]

        year_dict = {'19': [('--', '2019')], '20': [('--', '2020')], 
                        '21': [('--', '2021')],  '22': [('--', '2022')], 
                        '23': [('--', '2023')], '24': [('--', '2024')]}

        d1 = dict(year_dict[year])
        d1.update(dict(months))
        final_list = list(d1.items())
        return final_list

    t19 = SelectField(u'2019', validators=[DataRequired()], 
                            choices = choice_gen('19'), coerce=str, default = '2019')
    t20 = SelectField(u'2020', validators=[DataRequired()], 
                            choices = choice_gen('20'), coerce=str, default = '2020')
    t21 = SelectField(u'2021', validators=[DataRequired()], 
                            choices = choice_gen('21'), coerce=str, default = '2021')
    t22 = SelectField(u'2022', validators=[DataRequired()], 
                            choices = choice_gen('22'), coerce=str, default = '2022')
    t23 = SelectField(u'2023', validators=[DataRequired()], 
                            choices = choice_gen('23'), coerce=str, default = '2023')
    t24 = SelectField(u'2024', validators=[DataRequired()], 
                            choices = choice_gen('24'), coerce=str, default = '2024')

    submit = SubmitField('Go')