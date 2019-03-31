from database import db
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app import bcrypt


class User(db.Model):
    __tablename__ = 'user'

    email = Column(String, unique=True, nullable=False)
    password = Column(String(60), nullable=False)

    # TODO: Make it works
    permissions = relationship('modules.permission.models.UserPermission', backref='user')

    # TODO: Improve the way to do that
    # @password.setter
    # def setpassword(self, plaintext_password):
    #     self.password = bcrypt.generate_password_hash(plaintext_password)
