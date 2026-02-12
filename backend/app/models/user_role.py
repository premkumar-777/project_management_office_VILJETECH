# from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
# from app.database import Base
# from sqlalchemy.sql import func

# class UserRole(Base):
#     __tablename__ = "user_roles"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     role_id = Column(Integer, ForeignKey("roles.id"))
#     assigned_by = Column(Integer)
#     created_at = Column(TIMESTAMP, server_default=func.now())

# app/models/user_role.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    assigned_by = Column(Integer)

    created_at = Column(TIMESTAMP, server_default=func.now())

    # 🔗 Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role")
