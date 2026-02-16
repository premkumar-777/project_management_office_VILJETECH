from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    description = Column(String(500))

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    location = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)

    status_id = Column(Integer, ForeignKey("project_status.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    status = relationship("ProjectStatus")
    client = relationship("Client")
    members = relationship("ProjectMember", back_populates="project")
