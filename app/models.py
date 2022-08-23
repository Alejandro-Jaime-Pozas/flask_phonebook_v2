from app import db, login # from app folder, import db from __init__
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# class for user database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    addresses = db.relationship('Address', backref='owner', lazy='dynamic') # relationship w Address class

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self) 
        db.session.commit() 

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def __repr__(self):
        return f'<User | {self.email}>'


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id) # COME BACK TO TRY TO UNDERSTAND THIS


#create a class for the Address db where columns are specified for the sql database tables...
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # links to User class/table


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self) 
        db.session.commit() 

    def __repr__(self):
        return f'<Address for | {self.name}'

    # method to edit the contact's name, phone, or address
    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k in {'name', 'phone', 'address'}:
                setattr(self, k, v) # COME BACK TO TRY TO UNDERSTAND THIS
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()