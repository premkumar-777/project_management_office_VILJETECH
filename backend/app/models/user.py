from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from .user_status import UserStatus

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    status_id = Column(Integer, ForeignKey("user_status.id"))
    location = Column(String(100))
    created_by = Column(Integer)
    deleted_by = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    mfa_secret = Column(String(255), nullable=True)
    mfa_enabled = Column(Boolean, default=False)

    # Relationships
    status = relationship("UserStatus", backref="users")

    # Roles assigned to this user
    roles = relationship(
        "UserRole",
        back_populates="user",
        foreign_keys="[UserRole.user_id]",
        cascade="all, delete-orphan"
    )

    # Roles this user assigned to others
    assigned_roles = relationship(
        "UserRole",
        back_populates="assigned_by_user",
        foreign_keys="[UserRole.assigned_by]"
    )

