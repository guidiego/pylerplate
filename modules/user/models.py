import enum

from app import bcrypt
from database import db
from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey, Enum
from sqlalchemy.orm import relationship

from utils.errors import AuthenticationError


class PermissionEnum(enum.Enum):
    ADMIN = 0
    COMMON = 1


class UserPermission(db.Model):
    __tablename__ = 'user_group'

    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    permission = Column(Enum(PermissionEnum), nullable=False)

    @classmethod
    def set_common(cls, user_id):
        return cls(
            user_id=user_id,
            permission=PermissionEnum.COMMON,
        )

    @classmethod
    def set_admin(cls, user_id):
        return cls(
            user_id=user_id,
            permission=PermissionEnum.ADMIN,
        )


class User(db.Model):
    __tablename__ = 'user'

    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(LargeBinary(60), nullable=False)

    permissions = relationship(UserPermission, backref='user')

    def pre_save(self):
        self.password = bcrypt.generate_password_hash(self.password)

    @classmethod
    def verify_credentials(cls, email, password):
        user = cls.query.filter(
            cls.email == email,
        ).first()

        if user is not None and bcrypt.check_password_hash(user.password, password):
            return user

        raise AuthenticationError(error_code=3)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(
            cls.email == email,
        ).first()

    @classmethod
    def get_all(cls, workspace=None, page=None, user=None, limit=None, q=None):
        q = q or cls.query
        q = cls.get_only_available(q)

        if limit is None:
            limit = '10'
    
        if page is None:
            page = '1'

        return q.paginate(int(page), int(limit), False)
