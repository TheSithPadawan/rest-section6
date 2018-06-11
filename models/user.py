'''
A module that interacts with the database
model: backend -- internal representation
resources: -- interacts with the client
'''
import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()

    # classmethod is kind of like Java static method?
    # cls refers to current class
    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

