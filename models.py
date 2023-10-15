from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app    
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    '''Users'''
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)
    password = db.Column(db.String,
                         nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)