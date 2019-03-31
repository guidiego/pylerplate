import enum

from database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import db


class User(db.Model):
    __tablename__ = 'user'

    email = Column(String, unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    permissions = relationship('UserPermission', backref='user')

    # TODO: Improve the way to do that
    # @password.setter
    # def setpassword(self, plaintext_password):
    #     self.password = bcrypt.generate_password_hash(plaintext_password)


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