from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Default expiry values
TEMP_TOKEN_EXPIRE_MINUTES = 5
INVITE_TOKEN_EXPIRE_HOURS = 24
RESET_TOKEN_EXPIRE_MINUTES = 10

# 🔐 Password helpers
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🎟️ Generic temp token creator (MFA / Invite / Reset)
def create_temp_token(
    user_id: int,
    expires_minutes: int = TEMP_TOKEN_EXPIRE_MINUTES,
    token_type: str = "mfa"
):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    payload = {
        "user_id": user_id,
        "type": token_type,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# 📧 Invite token (first time password setup)
def create_invite_token(user_id: int):
    expire_minutes = INVITE_TOKEN_EXPIRE_HOURS * 60
    return create_temp_token(user_id, expire_minutes, "invite")


# 🔁 Password reset token
def create_reset_token(user_id: int):
    return create_temp_token(user_id, RESET_TOKEN_EXPIRE_MINUTES, "reset")
