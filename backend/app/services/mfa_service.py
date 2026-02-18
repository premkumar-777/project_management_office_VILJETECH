import pyotp
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.password_reset import PasswordReset
from app.services.password_reset_service import send_forgot_password_otp, verify_otp as base_verify_otp
from app.core.security import hash_password

ACTIVE_STATUS_ID = 2  # Only active users
OTP_EXPIRY_MINUTES = 5

def regenerate_mfa_qr(db: Session, email: str, otp: str):
    """
    Verify OTP and generate new MFA secret + QR URI for active users
    """

    # ✅ Step 1: Verify OTP
    base_verify_otp(db, email, otp)  # will raise HTTPException if invalid

    # ✅ Step 2: Fetch user and check active
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status_id != ACTIVE_STATUS_ID:
        raise HTTPException(status_code=403, detail="User not active")

    # ✅ Step 3: Generate new MFA secret
    mfa_secret = pyotp.random_base32()

    # ✅ Step 4: Generate QR URI (frontend can generate QR code from this)
    qr_uri = pyotp.TOTP(mfa_secret).provisioning_uri(
        name=f"{user.email}",
        issuer_name="PMO-Platform"
    )

    # ✅ Step 5: Update user in database
    user.mfa_secret = mfa_secret
    db.commit()

    return {
        "success": True,
        "message": "OTP verified. MFA secret updated.",
        "data": {
            "mfa_required": True,
            "qr_uri": qr_uri
        }
    }
