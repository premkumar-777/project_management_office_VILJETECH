# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from app.database import SessionLocal
# # from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
# # from app.services.auth_service import authenticate, verify_mfa

# # router = APIRouter(prefix="/auth", tags=["Authentication"])

# # # ------------------------------
# # # DB dependency
# # # ------------------------------
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # # ------------------------------
# # # Login endpoint
# # # ------------------------------
# # @router.post("/login")
# # def login(data: LoginRequest, db: Session = Depends(get_db)):
# #     result = authenticate(db, data.email, data.password)

# #     if not result:
# #         raise HTTPException(status_code=401, detail="Invalid credentials")

# #     return result

# # # ------------------------------
# # # Verify MFA endpoint
# # # ------------------------------
# # @router.post("/verify-mfa")
# # def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db)):
# #     result = verify_mfa(db, data.temp_token, data.otp)
# #     if not result:
# #         raise HTTPException(status_code=401, detail="Invalid token or OTP")
# #     return result

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
# from app.services.auth_service import authenticate, verify_mfa

# router = APIRouter(prefix="/auth", tags=["Authentication"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Login endpoint
# @router.post("/login")
# def login(data: LoginRequest, db: Session = Depends(get_db)):
#     result = authenticate(db, data.email, data.password)
#     if not result:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return result

# # Verify MFA endpoint
# # @router.post("/verify-mfa")
# # def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db)):
# #     access_token, error = verify_mfa(db, data.temp_token, data.otp)
# #     if error:
# #         raise HTTPException(status_code=401, detail=error)
# #     return access_token

# @router.post("/verify-mfa")
# def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db())):
#     access_data, error = verify_mfa(db, data.temp_token, data.otp)
#     if error:
#         raise HTTPException(status_code=401, detail=error)
#     return access_data

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
from app.services.auth_service import authenticate, verify_mfa

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ------------------------------
# DB dependency
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# Login endpoint
# ------------------------------
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = authenticate(db, data.email, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result

# ------------------------------
# Verify MFA endpoint
# ------------------------------
@router.post("/verify-mfa")
def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db)):
    access_data, error = verify_mfa(db, data.temp_token, data.otp)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return access_data
