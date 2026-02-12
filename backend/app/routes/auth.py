
# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import SetPassword
from app.schemas.auth_schema import LoginRequest, MFAVerifyRequest
from app.services.auth_service import authenticate, verify_mfa, set_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ------------------------------
# Login Endpoint
# ------------------------------
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint
    Handles:
      - Password check
      - MFA check
      - First-time MFA setup
    """
    result = authenticate(db, request.email, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return result


# ------------------------------
# Set Password (first-time)
# ------------------------------
@router.post("/set-password")
def set_user_password(request: SetPassword, db: Session = Depends(get_db)):
    """
    First-time password setup using temp_token
    """
    result, error = set_password(db, request.temp_token, request.password)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


# ------------------------------
# MFA Verification
# ------------------------------
@router.post("/verify-mfa")
def verify_mfa_endpoint(request: MFAVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP for MFA and return final access token
    """
    access_data, error = verify_mfa(db, request.temp_token, request.otp)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return access_data
