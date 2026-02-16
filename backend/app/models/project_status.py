from sqlalchemy import Column, Integer, String
from app.database import Base

class ProjectStatus(Base):
    __tablename__ = "project_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
