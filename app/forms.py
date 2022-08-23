# Use the actual name, phone, address fields here. additional also a remember me, and submit button
from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pswd = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    # pass

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    # ADD REMEMBER ME LATER
    submit = SubmitField()

class AddContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired(), Length(min=7, max=14)])
    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField('Add Contact')

    # def clean_phone(self):
    #     for digit in self.phone.data:
    #         if digit.isdigit():