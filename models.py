from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app    
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    '''Users'''
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"{u.user_id} {u.username}"
    
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

class Player(db.Model):
    '''Players'''
    __tablename__ = 'Players'

    def __repr__(self):
        p = self
        return f"{p.player_id} {p.name} {p.user_id}"
    
    player_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    name = db.Column(db.String,
                     nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id', ondelete='cascade'))
    team_id = db.Column(db.Integer,
                    db.ForeignKey('teams.team_id', ondelete='cascade'))

    
class Team(db.Model):
    '''Teams'''
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = db.Column(db.String,
                        nullable=False)
    sport = db.Column(db.String,
                      nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id', ondelete='cascade'))