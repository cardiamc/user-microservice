import datetime as dt
import json
from random import randint

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property

from werkzeug.security import check_password_hash, generate_password_hash

DATABASE_NAME = 'sqlite:///users.db'

db = SQLAlchemy()


'''
Models the "following" relationship as a many-to-many relationship from
and to the Users table. 
Primary key is composed by both the foreign keys.
'''
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True),
    db.Column('followee_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True)
)


class User(db.Model):
    '''
    Models the user of the application.
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode(128), unique=True, nullable=False)
    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    telegram_chat_id = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    # All operations on the relationship can be done via the this property that
    # lazily exposes the list of followed users or the followed property that
    # provides the list of followees.
    follows = db.relationship('User', secondary=followers,
                              primaryjoin=id == followers.c.follower_id,
                              secondaryjoin=id == followers.c.followee_id,
                              lazy='subquery',
                              backref=db.backref('followed', lazy=True))

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        salt = randint(16, 32)
        self.password = generate_password_hash(password, salt_length=salt)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname
        }
