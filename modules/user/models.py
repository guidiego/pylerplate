from database import Base, db
from sqlalchemy import Column, String, Binary

from app import bcrypt


class User(Base, db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Binary(60), nullable=False)

    def __init__(self, *args, **kwargs):
        self.email = kwargs['email']
        self.password = kwargs['password']

    @password.setter
    def setpassword(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password)
