from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    language = db.Column(db.String(2), unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    username = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120),  unique = False) 

    def __repr__(self):
        return '<User %r>' % (self.nickname)
