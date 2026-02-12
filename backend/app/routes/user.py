# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user_schema import UserCreateRequest
from app.services.user_service import create_user
from app.core.auth_dependency import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_user(
    data: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Super-admin or admin adds a new user (without password).
    User will receive email/create-password flow separately.
    """

    # 🔹 Permission check using role_names from auth_dependency
    if "super admin" not in current_user.role_names and "admin" not in current_user.role_names:
        raise HTTPException(status_code=403, detail="You cannot add users")

    # 🔹 Admin restrictions
    if "admin" in current_user.role_names:
        if 1 in data.roles:  # 1 = Super Admin
            raise HTTPException(status_code=403, detail="Admin cannot create super-admin")
        if 2 in data.roles:  # 2 = Admin
            raise HTTPException(status_code=403, detail="Admin cannot create another admin")

    # 🔹 Create user
    new_user = create_user(
        db,
        creator_id=current_user.id,
        name=data.name,
        email=data.email,
        roles=data.roles,
        location=data.location,
        status_id=data.status_id  # default = 1 pending
    )

    # 🔹 Generate temp token for first-time login
    from app.core.security import create_temp_token
    temp_token = create_temp_token(new_user["id"])

    # 🔹 Return invitation info (to send in email in future)
    invite_url = f"http://localhost:3000/set-password?token={temp_token}"

    return {
        "message": "User created successfully",
        "user_id": new_user["id"],
        "temp_token": temp_token,
        "invite_url": invite_url
    }
