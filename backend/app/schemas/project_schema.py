from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    client_email: str
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status_id: int

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status_id: int

    class Config:
        from_attributes = True


class InviteEmployees(BaseModel):
    employee_ids: List[int]
