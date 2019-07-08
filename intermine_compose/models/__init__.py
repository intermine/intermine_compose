from .base import db
from .users import User

def init_app(app):
    db.init_app(app)

def create_all_tables():
    db.create_all()

def drop_all_tables():
    db.drop_all()