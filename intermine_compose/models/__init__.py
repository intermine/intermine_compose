from .base import db, ma
from .users import User
from .data import DataFile
from .mine import Mine
from .templates import Template
from .build import Build

def init_app(app):
    db.init_app(app)
    ma.init_app(app)


def create_all_tables():
    db.create_all()

def drop_all_tables():
    db.drop_all()