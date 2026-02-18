# create_tables.py

from app.database import Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.client import Client
from app.models.user_status import UserStatus
from app.models.project import Project
from app.models.project_status import ProjectStatus
from app.models.project_member import ProjectMember


# Create all tables in selected DB
Base.metadata.create_all(engine)

print("✅ All tables created in Azure PMO_DATABASE!")
