from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user_roles = relationship("UserRole", back_populates="role")
