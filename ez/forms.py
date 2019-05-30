from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class Expend(FlaskForm):
    amount = FloatField(validators=[DataRequired()])
    category_choices = [('Category', 'Category'), ('Placeholder1', 'Placeholder1')]
    category = SelectField(u'Month', validators=[DataRequired()], choices = category_choices, coerce=str, default = 'Category')
    note = TextAreaField()
    submit = SubmitField('Submit Expense')
