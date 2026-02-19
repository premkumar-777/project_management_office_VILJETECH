import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.password_reset import PasswordReset
from app.core.security import hash_password


OTP_EXPIRY_MINUTES = 5
ACTIVE_STATUS_ID = 2


def generate_otp():
    return str(random.randint(100000, 999999))


# ================================
# 📌 STEP 1 — SEND OTP
# ================================
def send_forgot_password_otp(db: Session, email: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")

    if user.status_id != ACTIVE_STATUS_ID:
        raise HTTPException(status_code=403, detail="Your account is not active")

    # 🧹 delete old OTPs
    db.query(PasswordReset).filter(PasswordReset.email == email).delete()
    db.commit()

    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    reset_entry = PasswordReset(
        user_id=user.id,
        email=email,
        otp=otp,
        expires_at=expiry,
        verified=False
    )

    db.add(reset_entry)
    db.commit()

    # 👉 integrate email service here
    print("OTP:", otp)

    return {
        "success": True,
        "message": "OTP sent successfully",
        "data": {
            "email": email,
            "expires_in": OTP_EXPIRY_MINUTES * 60
        }
    }


# ================================
# 📌 STEP 2 — VERIFY OTP
# ================================
def verify_otp(db: Session, email: str, otp: str):

    record = (
        db.query(PasswordReset)
        .filter(PasswordReset.email == email)
        .order_by(PasswordReset.created_at.desc())
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="OTP not found")

    # ⏱️ expired
    if record.expires_at < datetime.utcnow():
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    # ❌ invalid
    if record.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # ✅ mark verified
    record.verified = True
    db.commit()

    return {
        "success": True,
        "message": "OTP verified successfully"
    }


# ================================
# 📌 STEP 3 — RESET PASSWORD
# ================================
def reset_password(db: Session, email: str, new_password: str):

    record = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.email == email,
            PasswordReset.verified == True
        )
        .order_by(PasswordReset.created_at.desc())
        .first()
    )

    if not record:
        raise HTTPException(status_code=400, detail="OTP not verified")

    # extra safety → check expiry again
    if record.expires_at < datetime.utcnow():
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(new_password)

    # 🧹 delete OTP record after success
    db.delete(record)
    db.commit()

    return {
        "success": True,
        "message": "Password updated successfully"
    }
