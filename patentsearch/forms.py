from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
    url, ValidationError

from patentsearch.models import User

#search form class
class SearchForm(Form):
    searchtext = StringField('Text (across all fields)')
    country = StringField('Country')
    #author = StringField('author') #potentially senstive data - not to be used (legal considerations)
    patentnumber = StringField('Patent Number')
    cpcs = StringField('Kind')
    organization = StringField('Company')
    sortby = SelectField(u'Sort by ', choices=[('score', 'score'), ('date', 'date')])
    skip = IntegerField('Skip')
    recordnumber = SelectField(u'Return Count', choices=[('10', '10'), ('20', '20'), ('30', '30')])

#Login form class
class LoginForm(Form):
    username = StringField('User Name:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

#Signup form with validators
class SignupForm(Form):
    username = StringField('Username',
                    validators=[
                        DataRequired(), Length(3, 80),
                        Regexp('^[A-Za-z0-9_]{3,}$',
                            message='Usernames consist of numbers, letters,'
                                    'and underscores.')])
    password = PasswordField('Password',
                    validators=[
                        DataRequired(),
                        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('A user with this email address already exists.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('Popular User name, apologies it has already been taken.')
