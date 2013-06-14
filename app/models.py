from app import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, \
     check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1

def init_db():
    u1 = models.User(username='admin', language='en', email='admin@email.com', password='jobs', role=models.ROLE_ADMIN)
    u2 = models.User(username='susan', language='fr', email='john@email.com', password='jojo', role=models.ROLE_USER)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

def clear_db():
    db.session.drop_all()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    language = db.Column(db.String(2), unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    username = db.Column(db.String(120), index = True, unique = True)
    _password = db.Column('password', db.String(120),  unique = False) 

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

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
