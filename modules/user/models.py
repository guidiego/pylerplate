import enum

from app import bcrypt
from database import db
from sqlalchemy import Column, String, Integer, Binary, ForeignKey, Enum
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'user'

    email = Column(String, unique=True, nullable=False)
    password = Column(Binary(60), nullable=False)
    permissions = relationship('UserPermission', backref='permissions')

    def pre_save(self):
        self.password = bcrypt.generate_password_hash(self.password)

class PermissionEnum(enum.Enum):
    ADMIN = 0
    COMMON = 1

class UserPermission(db.Model):
    __tablename__ = 'user_group'

    user_id = Column(Integer, ForeignKey('user.id'))
    permission = Column(Enum(PermissionEnum), nullable=False)

    @classmethod
    def set_common(cls, user_id):
        return cls(
            user_id=user_id,
            permission=PermissionEnum.COMMON
        )