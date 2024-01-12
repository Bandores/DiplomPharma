from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class EditForm(FlaskForm):
    title = StringField('Title')
    price = IntegerField('Price')
    details = TextAreaField('Details')
    img = StringField('Image URL')
    total = IntegerField('Total')
class SearchedForm(FlaskForm):
    searched = StringField('Search')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email',validators=[DataRequired(),Email()])
    phone = IntegerField('Номер телефона',validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    password = PasswordField('Пароль',validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
