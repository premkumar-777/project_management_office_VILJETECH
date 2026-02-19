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
    temp_token: str
    email: str
    name: str
    password: str  # This is the "new_password"

class MFARequest(BaseModel):
    temp_token: str
    otp: str

    