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

    # 🔹 Load current user roles
    user_roles = [r.role for r in current_user.roles]  # list of role names

    # 🔹 Permission check
    if "super-admin" not in user_roles and "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="You cannot add users")

    # 🔹 Admin cannot create super-admin or admin
    if "admin" in user_roles:
        if 1 in data.roles:  # 1 = super-admin
            raise HTTPException(status_code=403, detail="Admin cannot create super-admin")
        if 2 in data.roles:  # 2 = admin
            raise HTTPException(status_code=403, detail="Admin cannot create another admin")

    # 🔹 Call service to create user
    new_user = create_user(
        db,
        creator_id=current_user.id,
        name=data.name,
        email=data.email,
        roles=data.roles,
        location=data.location,
        status_id=data.status_id
    )

    return {"message": "User created successfully", "user_id": new_user["id"]}
