from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, \
     check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    language = Column(String(2), unique = False)
    email = Column(String(120), index = True, unique = True)
    role = Column(SmallInteger, default = ROLE_USER)
    username = Column(String(120), index = True, unique = True)
    _password = Column('password', String(120),  unique = False)

    def __init__(self, username, password, language, email, role):
        self.username = username
        self.set_password(password)
        self.language = language
        self.email = email
        self.role = role


    def _get_password(self):
        return self._password

    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

