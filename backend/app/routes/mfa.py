import pyotp
import qrcode
import base64
from io import BytesIO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.password_reset_schema import RegenerateMFARequest
from app.services.mfa_service import regenerate_mfa_qr

router = APIRouter(prefix="/mfa", tags=["MFA"])


@router.post("/setup/{user_id}")
def setup_mfa(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return {"error": "User not found"}

    # Generate secret
    secret = pyotp.random_base32()
    user.mfa_secret = secret
    db.commit()

    # Generate QR
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="ViljeTech PMO"
    )

    qr = qrcode.make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return {
        "qr_code": f"data:image/png;base64,{img_str}",
        "secret": secret
    }

@router.post("/verify/{user_id}")
def verify_mfa(user_id: int, otp: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.mfa_secret:
        return {"error": "Invalid user"}

    totp = pyotp.TOTP(user.mfa_secret)

    if totp.verify(otp):
        user.mfa_enabled = True
        db.commit()
        return {"message": "MFA Enabled Successfully"}
    else:
        return {"error": "Invalid OTP"}

@router.post("/regenerate-qr")
def regenerate_qr(request: RegenerateMFARequest, db: Session = Depends(get_db)):
    """
    Step 1: User requests new MFA QR → send OTP
    Step 2: Provide OTP as query/body → generate new secret + QR
    """
    return regenerate_mfa_qr(db, request.email, request.otp)
    
