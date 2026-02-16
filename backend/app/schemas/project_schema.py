from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List


# -----------------------------
# Create Project
# -----------------------------
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    client_email: EmailStr
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status_id: int


# -----------------------------
# Assign Members
# -----------------------------
class MemberAssign(BaseModel):
    user_id: int
    role_id: int


class AssignMembersRequest(BaseModel):
    members: List[MemberAssign]
