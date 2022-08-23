# this is outside of the app folder bc of circular import, want to be able to import config
import os
basedir = os.path.abspath(os.path.dirname(__file__)) # this stores basedir in the main dir of this application (phone_flask)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET-KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # this is where the sql database lives
    SQLALCHEMY_TRACK_MODIFICATIONS = False # set to false bc we do not need to send a signal to the app every time a change is to be made...
