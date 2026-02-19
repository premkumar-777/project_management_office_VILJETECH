from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import verify_password, hash_password, create_access_token, create_temp_token, create_refresh_token
from app.sql import queries
import pyotp
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM


def authenticate(db: Session, email: str, password: str):
    conn = db.connection()

    # 🔹 1️⃣ Check internal user
    user = conn.execute(text(queries.GET_USER_BY_EMAIL), {"email": email}).fetchone()

    if user and user.password_hash and verify_password(password, user.password_hash):
        roles = conn.execute(text(queries.GET_USER_ROLES), {"user_id": user.id}).fetchall()
        role_list = [r[0] for r in roles]

        if user.mfa_enabled:
            temp_token = create_temp_token(user.id)
            return {
                "success": True,
                "message": "MFA required",
                "data": {
                    "mfa_required": True,
                    "temp_token": temp_token,
                    "roles": role_list
                }
            }

        access_token = create_access_token({
            "id": user.id,
            "type": "user",
            "roles": role_list
        })

        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "roles": role_list
            }
        }

    # 🔹 2️⃣ First-time login
    if user and (user.status_id == 1 or not user.password_hash):
        return {
            "success": True,
            "message": "First time login - password setup required",
            "data": {
                "mfa_required": True,
                "first_time": True,
                "user_id": user.id,
                "roles": []
            }
        }

    # 🔹 3️⃣ Check client
    client = conn.execute(text(queries.GET_CLIENT_BY_EMAIL), {"email": email}).fetchone()
    if client and verify_password(password, client.password_hash):
        access_token = create_access_token({
            "id": client.id,
            "type": "client",
            "roles": ["client"]
        })

        return {
            "success": True,
            "message": "Client login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "roles": ["client"]
            }
        }

    # 🔹 4️⃣ Invalid credentials
    return {
        "success": False,
        "message": "Invalid email or password",
        "data": None
    }

def set_password(db: Session, temp_token: str, new_password: str):
    try:
        payload = jwt.decode(temp_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return {"success": False, "message": "Invalid token", "data": None}
    except JWTError:
        return {"success": False, "message": "Invalid token", "data": None}

    conn = db.connection()
    user = conn.execute(
        text("SELECT * FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    ).fetchone()

    if not user:
        return {"success": False, "message": "This email is not registered in our services", "data": None}
    if user.status_id != 1:  # invited/pending
        return {"success": False, "message": "User already registered or not allowed", "data": None}

    password_hash = hash_password(new_password)
    mfa_secret = pyotp.random_base32()
    qr_uri = pyotp.TOTP(mfa_secret).provisioning_uri(
        name=f"user{user_id}@pmo.com", issuer_name="PMO-Platform"
    )

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
        "success": True,
        "message": "Registration completed. Scan QR for MFA",
        "data": {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "mfa_required": True,
            "qr_uri": qr_uri
        }
    }
def verify_mfa(db: Session, temp_token: str, otp: str):
    try:
        payload = jwt.decode(temp_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return {
            "success": False,
            "message": "Invalid token",
            "data": None
        }

    user_id = payload.get("user_id")
    if not user_id:
        return {
            "success": False,
            "message": "Invalid token payload",
            "data": None
        }

    conn = db.connection()
    user = conn.execute(
        text(queries.GET_USER_BY_ID),
        {"user_id": user_id}
    ).fetchone()

    if not user or not user.mfa_enabled:
        return {
            "success": False,
            "message": "MFA not configured",
            "data": None
        }

    totp = pyotp.TOTP(user.mfa_secret)

    if not totp.verify(str(otp).strip(), valid_window=1):
        return {
            "success": False,
            "message": "Invalid OTP",
            "data": None
        }

    # ✅ roles
    roles = conn.execute(
        text(queries.GET_USER_ROLES),
        {"user_id": user.id}
    ).fetchall()

    role_list = [r[0] for r in roles]

    # ✅ tokens
    token_payload = {
        "id": user.id,
        "type": "user",
        "roles": role_list
    }

    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)

    return {
        "success": True,
        "message": "MFA verified successfully",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },
            "roles": role_list
        }
    }

def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return {
            "success": False,
            "message": "Invalid refresh token",
            "data": None
        }

    if payload.get("token_type") != "refresh":
        return {
            "success": False,
            "message": "Invalid token type",
            "data": None
        }

    user_id = payload.get("id")
    roles = payload.get("roles", [])

    conn = db.connection()
    user = conn.execute(
        text(queries.GET_USER_BY_ID),
        {"user_id": user_id}
    ).fetchone()

    if not user:
        return {
            "success": False,
            "message": "User not found",
            "data": None
        }

    new_access_token = create_access_token({
        "id": user_id,
        "type": "user",
        "roles": roles
    })

    new_refresh_token = create_refresh_token({
        "id": user_id,
        "type": "user",
        "roles": roles
    })

    return {
        "success": True,
        "message": "Token refreshed successfully",
        "data": {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },
            "roles": roles
        }
    }
