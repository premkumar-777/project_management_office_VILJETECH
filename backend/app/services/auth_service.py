from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import verify_password, create_access_token, create_temp_token
from app.sql import queries
import pyotp
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM


def authenticate(db: Session, email: str, password: str):
    """
    Authenticate a user (super-admin/admin/employee) or client.
    Handles MFA and returns either:
      - temp_token if MFA is enabled
      - access_token if MFA not enabled
    """
    conn = db.connection()

    # ------------------------------
    # 🔹 Check Internal User
    # ------------------------------
    user = conn.execute(text(queries.GET_USER_BY_EMAIL), {"email": email}).fetchone()
    if user and verify_password(password, user.password_hash):

        # Fetch user roles
        roles = conn.execute(text(queries.GET_USER_ROLES), {"user_id": user.id}).fetchall()
        role_list = [r[0] for r in roles]

        # ------------------------------
        # 🔐 MFA CHECK
        # ------------------------------
        if user.mfa_enabled:
            temp_token = create_temp_token(user.id)
            return {
                "mfa_required": True,
                "temp_token": temp_token
            }

        # ------------------------------
        # ✅ Normal login (MFA not enabled)
        # ------------------------------
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

    # ------------------------------
    # 🔹 Check Client
    # ------------------------------
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

    # ------------------------------
    # ❌ Invalid credentials
    # ------------------------------
    return None

def verify_mfa(db: Session, temp_token: str, otp: str):
    """
    Verify OTP for MFA and return final access token.
    Returns: (access_data, error_message)
    """

    # 1️⃣ Decode token
    try:
        payload = jwt.decode(temp_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None, "Invalid token"

    user_id = payload.get("user_id")
    mfa_flag = payload.get("mfa")

    # Strict validation
    if user_id is None:
        return None, "Invalid token"

    if mfa_flag is not True:
        return None, "Invalid token"

    # 2️⃣ Fetch user
    conn = db.connection()
    user = conn.execute(
        text(queries.GET_USER_BY_ID),
        {"user_id": user_id}
    ).fetchone()

    if not user:
        return None, "User not found"

    if not user.mfa_enabled:
        return None, "MFA not configured"

    # 3️⃣ Verify OTP
    totp = pyotp.TOTP(user.mfa_secret)
    clean_otp = str(otp).strip()
    # small time drift tolerance
    if not totp.verify(clean_otp, valid_window=1):
        return None, "Invalid OTP"
    
    # 4️⃣ Generate final access token
    roles = conn.execute(
        text(queries.GET_USER_ROLES),
        {"user_id": user.id}
    ).fetchall()

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
