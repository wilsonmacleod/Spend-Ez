from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class Expend(FlaskForm):
    amount = FloatField(validators=[DataRequired()])
    category_choices = [('Category', 'Category'), ('Placeholder1', 'Placeholder1')]
    category = SelectField(u'Month', choices = category_choices, coerce=str, default = 'Category')
    note = StringField('Notes?')
    submit = SubmitField('Submit Expense')
