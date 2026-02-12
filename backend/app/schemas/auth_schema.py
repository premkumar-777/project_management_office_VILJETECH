from pydantic import BaseModel, EmailStr
from typing import List

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class MFAVerifyRequest(BaseModel):
    temp_token: str
    otp: str
