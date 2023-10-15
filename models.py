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
    user_id = db.Column(db.Integer,
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

class Activity(db.Model):
    __tablename__ = 'activites'
    '''Activities'''
    activity_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    name = db.Column(db.String,
                     nullable=False)
    type = db.Column(db.String,
                     nullable=False)
    distance = db.Column(db.Integer,
                         nullable=False)
    date = db.Column(db.Date,
                     nullable=False)
    time = db.column(db.Time,
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id', ondelete='cascade'))
    
class Comments(db.Model):
    __tablename__ = 'comments'
    '''Comments'''
    comment_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    comment = db.Column(db.String,
                        nullable=False)
    user_id = db.Column(db.Integer,
                db.ForeignKey('users.user_id', ondelete='cascade'))
    activity_id = db.Column(db.Integer,
                            db.ForeignKey('activities.activity_id', ondelete='cascade'))
    
class Likes(db.Model):
    __tablename__ = 'likes'
    '''Likes'''
    like_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.user_id', ondelete='cascade'))
    activity_id = db.Column(db.Integer,
                        db.ForeignKey('activities.activity_id', ondelete='cascade'))