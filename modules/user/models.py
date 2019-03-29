import datetime
import random
import string

from database import Base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy import Column, DateTime, Integer, Text, String, Binary, text

from app import bcrypt

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(Binary(60), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, server_default=text("NOW()"))
    updated_at = Column(
        DateTime,
        onupdate=datetime.datetime.now, nullable=True, server_default=text("NULL ON UPDATE NOW()")
    )
    deleted_at = Column(DateTime)

    def __init__(self, *args, **kwargs):
        self.email = kwargs['email']
        self._password = kwargs['password']

    @hybrid_property
    def _password(self):
        return self.password

    @_password.setter
    def set_password(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password)
