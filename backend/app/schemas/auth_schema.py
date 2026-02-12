from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    roles: list[str]

class MFAVerifyRequest(BaseModel):
    temp_token: str
    otp: str
# from pydantic import BaseModel, EmailStr
# from typing import List

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# class MFAVerifyRequest(BaseModel):
#     temp_token: str
#     otp: str
