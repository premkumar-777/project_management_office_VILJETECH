# app/schemas/user_schema.py
from pydantic import BaseModel
from typing import List, Optional

class UserCreateRequest(BaseModel):
    name: str
    email: str
    roles: List[int]      # role IDs
    location: str
    status_id: Optional[int] = 1  # pending by default

class SetPassword(BaseModel):
    password: str
    temp_token: str

class MFARequest(BaseModel):
    temp_token: str
    otp: str

    