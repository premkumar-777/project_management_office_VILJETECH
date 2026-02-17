from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database import Base


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)

    # 🔗 Link to users table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    email = Column(String(150), nullable=False)
    otp = Column(String(6), nullable=False)

    expires_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship
    user = relationship("User", backref="password_resets")

    
