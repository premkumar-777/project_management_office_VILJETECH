# app/services/auth_service.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import verify_password, hash_password, create_access_token, create_temp_token
from app.sql import queries
import pyotp
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM

def authenticate(db: Session, email: str, password: str):
    """
    Authenticate a user (internal or client)
    MFA is ALWAYS required after password setup.
    Returns:
      • qr_uri (first-time login, pending user)
      • temp_token (MFA required)
      • access_token (for clients)
    """
    conn = db.connection()

    # 1️⃣ Check internal user
    user = conn.execute(text(queries.GET_USER_BY_EMAIL), {"email": email}).fetchone()
    if user and user.password_hash and verify_password(password, user.password_hash):
        roles = conn.execute(text(queries.GET_USER_ROLES), {"user_id": user.id}).fetchall()
        role_list = [r[0] for r in roles]

        # MFA enabled → send temp token
        if user.mfa_enabled:
            temp_token = create_temp_token(user.id)
            return {
                "mfa_required": True,
                "temp_token": temp_token,
                "roles": role_list
            }

        # Should not happen: fallback
        access_token = create_access_token({
            "id": user.id,
            "type": "user",
            "roles": role_list
        })
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "roles": role_list
        }

    # 2️⃣ First-time login (pending user)
    if user and (user.status_id == 1 or not user.password_hash):
        return {
            "mfa_required": True,
            "first_time": True,
            "user_id": user.id,
            "roles": []
        }

    # 3️⃣ Check client
    client = conn.execute(text(queries.GET_CLIENT_BY_EMAIL), {"email": email}).fetchone()
    if client and verify_password(password, client.password_hash):
        access_token = create_access_token({
            "id": client.id,
            "type": "client",
            "roles": ["client"]
        })
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "roles": ["client"]
        }

    # 4️⃣ Invalid credentials
    return None


# def set_password(db: Session, user_id: int, new_password: str):
    """
    Set password for first-time login users.
    Generates MFA secret & enables MFA
    Returns a QR code URI for Google Authenticator
    """
    conn = db.connection()

    password_hash = hash_password(new_password)
    mfa_secret = pyotp.random_base32()  # Generate new secret
    qr_uri = pyotp.TOTP(mfa_secret).provisioning_uri(name=f"user{user_id}@pmo.com", issuer_name="PMO-Platform")

    # Update user
    conn.execute(
        text("""
        UPDATE users
        SET password_hash = :password_hash,
            mfa_secret = :mfa_secret,
            mfa_enabled = 1,
            status_id = 2
        WHERE id = :user_id
        """),
        {"password_hash": password_hash, "mfa_secret": mfa_secret, "user_id": user_id}
    )
    db.commit()

    return {
        "mfa_required": True,
        "qr_uri": qr_uri
    }
def set_password(db: Session, temp_token: str, new_password: str):
    """
    Set password for first-time login users.
    Decodes temp_token, generates MFA secret & enables MFA,
    Returns a QR code URI for Google Authenticator.
    """
    # Decode JWT temp_token to get user_id
    try:
        payload = jwt.decode(temp_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None, "Invalid token"
    except JWTError:
        return None, "Invalid token"

    # Hash the password
    password_hash = hash_password(new_password)
    # Generate MFA secret
    mfa_secret = pyotp.random_base32()
    # Generate QR URI
    qr_uri = pyotp.TOTP(mfa_secret).provisioning_uri(
        name=f"user{user_id}@pmo.com", issuer_name="PMO-Platform"
    )

    # Update user in DB
    conn = db.connection()
    conn.execute(
        text("""
        UPDATE users
        SET password_hash = :password_hash,
            mfa_secret = :mfa_secret,
            mfa_enabled = 1,
            status_id = 2
        WHERE id = :user_id
        """),
        {"password_hash": password_hash, "mfa_secret": mfa_secret, "user_id": user_id}
    )
    db.commit()

    return {"mfa_required": True, "qr_uri": qr_uri}, None

def verify_mfa(db: Session, temp_token: str, otp: str):
    """
    Verify OTP for MFA and return final access token.
    Returns: (access_data, error_message)
    """
    try:
        payload = jwt.decode(temp_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None, "Invalid token"

    user_id = payload.get("user_id")
    mfa_flag = payload.get("mfa")
    if user_id is None or mfa_flag is not True:
        return None, "Invalid token"

    conn = db.connection()
    user = conn.execute(text(queries.GET_USER_BY_ID), {"user_id": user_id}).fetchone()
    if not user or not user.mfa_enabled:
        return None, "MFA not configured"

    # Verify OTP
    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(str(otp).strip(), valid_window=1):
        return None, "Invalid OTP"

    # Generate final access token
    roles = conn.execute(text(queries.GET_USER_ROLES), {"user_id": user.id}).fetchall()
    role_list = [r[0] for r in roles]

    access_token = create_access_token({
        "id": user.id,
        "type": "user",
        "roles": role_list
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "roles": role_list
    }, None
