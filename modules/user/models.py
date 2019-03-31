from database import db
from sqlalchemy import Column, String

from app import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    password = Column(String(60), nullable=False)

    # @password.setter
    # def setpassword(self, plaintext_password):
    #     self.password = bcrypt.generate_password_hash(plaintext_password)
