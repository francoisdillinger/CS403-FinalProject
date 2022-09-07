from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(200), nullable = False, unique = True)
    last_name = db.Column(db.String(200), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = False, unique = True)

class Recipients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    file_name = db.Column(db.String(150), nullable = False)