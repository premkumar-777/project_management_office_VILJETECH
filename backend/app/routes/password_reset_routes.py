from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.password_reset_schema import (
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest
)
from app.services.password_reset_service import (
    send_forgot_password_otp,
    verify_otp,
    reset_password
)

router = APIRouter(prefix="/password", tags=["Password Reset"])


@router.post("/forgot")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return send_forgot_password_otp(db, request.email)


@router.post("/verify-otp")
def verify_password_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    return verify_otp(db, request.email, request.otp)


@router.post("/reset")
def reset_user_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db, request.email, request.new_password)
