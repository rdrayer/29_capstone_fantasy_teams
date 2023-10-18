from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app    
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    """Users"""
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
    email = db.Column(db.String(50),
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register new user w/hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate user exists and pw matches"""
        """Return User if valid, else, return false"""
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

class Player(db.Model):
    """Players"""
    __tablename__ = 'players'

    def __repr__(self):
        p = self
        return f"{p.player_id} {p.name} {p.user_id}"
    
    player_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    name = db.Column(db.String,
                     nullable=False)
    
    position = db.Column(db.String,
                         nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id', ondelete='cascade'))
    team_id = db.Column(db.Integer,
                    db.ForeignKey('teams.team_id', ondelete='cascade'))
    
    team = db.relationship('Team', backref='teams')

    
class Team(db.Model):
    """Teams"""
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
    
    user = db.relationship('User', backref='users')