from database import Base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, String, Binary

from app import bcrypt


class User(Base):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    password = Column(Binary(60), nullable=False)

    def __init__(self, *args, **kwargs):
        self.email = kwargs['email']
        self._password = kwargs['password']

    @hybrid_property
    def _password(self):
        return self.password

    @_password.setter
    def set_password(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password)
