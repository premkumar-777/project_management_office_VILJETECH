# # # from fastapi import APIRouter, Depends, HTTPException
# # # from sqlalchemy.orm import Session
# # # from app.database import SessionLocal
# # # from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
# # # from app.services.auth_service import authenticate, verify_mfa

# # # router = APIRouter(prefix="/auth", tags=["Authentication"])

# # # # ------------------------------
# # # # DB dependency
# # # # ------------------------------
# # # def get_db():
# # #     db = SessionLocal()
# # #     try:
# # #         yield db
# # #     finally:
# # #         db.close()

# # # # ------------------------------
# # # # Login endpoint
# # # # ------------------------------
# # # @router.post("/login")
# # # def login(data: LoginRequest, db: Session = Depends(get_db)):
# # #     result = authenticate(db, data.email, data.password)

# # #     if not result:
# # #         raise HTTPException(status_code=401, detail="Invalid credentials")

# # #     return result

# # # # ------------------------------
# # # # Verify MFA endpoint
# # # # ------------------------------
# # # @router.post("/verify-mfa")
# # # def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db)):
# # #     result = verify_mfa(db, data.temp_token, data.otp)
# # #     if not result:
# # #         raise HTTPException(status_code=401, detail="Invalid token or OTP")
# # #     return result

# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from app.database import SessionLocal
# # from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
# # from app.services.auth_service import authenticate, verify_mfa

# # router = APIRouter(prefix="/auth", tags=["Authentication"])

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # # Login endpoint
# # @router.post("/login")
# # def login(data: LoginRequest, db: Session = Depends(get_db)):
# #     result = authenticate(db, data.email, data.password)
# #     if not result:
# #         raise HTTPException(status_code=401, detail="Invalid credentials")
# #     return result

# # # Verify MFA endpoint
# # # @router.post("/verify-mfa")
# # # def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db)):
# # #     access_token, error = verify_mfa(db, data.temp_token, data.otp)
# # #     if error:
# # #         raise HTTPException(status_code=401, detail=error)
# # #     return access_token

# # @router.post("/verify-mfa")
# # def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db())):
# #     access_data, error = verify_mfa(db, data.temp_token, data.otp)
# #     if error:
# #         raise HTTPException(status_code=401, detail=error)
# #     return access_data

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
# from app.services.auth_service import authenticate, verify_mfa

# router = APIRouter(prefix="/auth", tags=["Authentication"])

# # ------------------------------
# # DB dependency
# # ------------------------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ------------------------------
# # Login endpoint
# # ------------------------------
# @router.post("/login")
# def login(data: LoginRequest, db: Session = Depends(get_db)):
#     result = authenticate(db, data.email, data.password)
#     if not result:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return result

# # ------------------------------
# # Verify MFA endpoint
# # ------------------------------
# @router.post("/verify-mfa")
# def verify_mfa_endpoint(data: MFAVerifyRequest, db: Session = Depends(get_db)):
#     access_data, error = verify_mfa(db, data.temp_token, data.otp)
#     if error:
#         raise HTTPException(status_code=401, detail=error)
#     return access_data

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

# -------------------------------
# Login Route
# -------------------------------
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Login user or client.
    If MFA is enabled, returns `mfa_required` and a temp_token.
    Otherwise, returns final access token directly.
    """
    result = auth_service.authenticate(db, email, password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if MFA is required
    if result.get("mfa_required"):
        return {
            "mfa_required": True,
            "temp_token": result["temp_token"]
        }

    # Normal login (MFA not enabled)
    return result


# -------------------------------
# Verify MFA Route
# -------------------------------
@router.post("/verify-mfa")
def verify_mfa(temp_token: str, otp: str, db: Session = Depends(get_db)):
    """
    Verify MFA OTP using temp_token.
    Returns final access token if successful.
    """
    access_data, error = auth_service.verify_mfa(db, temp_token, otp)

    if error:
        raise HTTPException(status_code=401, detail=error)

    return access_data
