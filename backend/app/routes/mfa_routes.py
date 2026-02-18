from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.password_reset_schema import RegenerateMFARequest
from app.services.mfa_service import regenerate_mfa_qr

router = APIRouter(prefix="/mfa", tags=["MFA"])

@router.post("/regenerate-qr")
def regenerate_qr(request: RegenerateMFARequest, db: Session = Depends(get_db)):
    """
    Step 1: User requests new MFA QR → send OTP
    Step 2: Provide OTP as query/body → generate new secret + QR
    """
    return regenerate_mfa_qr(db, request.email, request.otp)
    
