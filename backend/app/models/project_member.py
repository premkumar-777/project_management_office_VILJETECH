from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    assigned_by = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="members")

    # 👇 specify FK explicitly
    user = relationship("User", foreign_keys=[user_id], back_populates="project_members")

    assigned_user = relationship("User", foreign_keys=[assigned_by])

    role = relationship("Role")
