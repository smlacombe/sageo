from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from app import babel, app
from flask import Flask

db_engine = None
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = db_session.query_property()

from app.db_model.user import User, ROLE_ADMIN, ROLE_USER


def init_engine(db_uri):
    global db_engine
    db_engine = create_engine(db_uri)
    db_session.configure(bind=db_engine)

def init_db():
    Base.metadata.create_all(bind=db_engine)
    u1 = User(username='admin', language='en', email='admin@email.com', password='jobs', role=ROLE_ADMIN)
    u2 = User(username='susan', language='fr', email='john@email.com', password='jojo', role=ROLE_USER)
    db_session.add(u1)
    db_session.add(u2)
    db_session.commit()

def clear_db():
    Base.metadata.drop_all(bind=db_engine)

