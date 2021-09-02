from enum import unique
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False, unique = True) #nullable false means it cannot be empty and this helps in operations using flask_marshmallow too
    password = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable = False, unique = True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()