# I need the following:
    # sign up page/form for user
    # login page/form for user
    # add a contact page/form for user (phone)
    # logout option when logged in
    # view all contacts page, which could technically be home page, but better to do a separate page
# Finalize the phonebook application that you have been working on this week. The phonebook should have the following capabilities:
    # - Users can sign up to use your application
    # - A user can create new addresses that are associated with them (One to Many relationship between User and Address)
    # - A user should only be able to create an address if they are logged in
    # - A user should be able to view all of the addresses that they have added
    # - A user should be able to edit an address that they created
    # - A user should be able to delete an address that they created
    # - Logged out users attempting to create, edit, or delete an address should be redirected to the login page
    # - The UI/UX should be easy and intuitive. A simple navbar with working links, message flashing, etc.
# *Bonus* Host your application on Heroku
    #  trying to host application on heroku

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # install flask-sqlalchemy, then create database instance here of the app
migrate = Migrate(app, db) # install flask-migrate, then create migrate instance here of the app, linked to db
# create an instance of LoginManager to handle authentication for users
login = LoginManager(app)
login.login_view = 'login' # tells the login manager which endpoint to redirect if someone NOT logged in
login.login_message_category = 'danger'


from app import routes, models # need models to migrate/upgrade database...