from enum import Enum
from database import db
from sqlalchemy import Column, Integer, ForeignKey

from app import bcrypt

class PermissionEnum(Enum):
    COMMON = 'common'
    ADMIN = 'admin'

class UserPermission(db.Model):
    __tablename__ = 'user_group'

    user_id = Column(Integer, ForeignKey('user.id'))
    permission = Column(Enum(PermissionEnum), nullable=False)