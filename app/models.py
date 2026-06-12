from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role_id = Column(
        Integer,
        ForeignKey("roles.id")
    )

    is_active = Column(
        Boolean,
        default=True
    )