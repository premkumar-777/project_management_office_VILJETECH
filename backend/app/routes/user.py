# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user_schema import UserCreateRequest
from app.services.user_service import create_user
from app.core.auth_dependency import get_current_user
from app.templates.email_templates import get_invite_email
from app.core.email import send_email
from app.core.security import create_invite_token 


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
    Super-admin or admin adds a new user.
    User will receive invitation email to set password.
    """

    # 🔹 Permission check
    if "super admin" not in current_user.role_names and "admin" not in current_user.role_names:
        raise HTTPException(status_code=403, detail="You cannot add users")

    # 🔹 Admin restrictions
    if "admin" in current_user.role_names:
        if 1 in data.roles:
            raise HTTPException(status_code=403, detail="Admin cannot create super-admin")
        if 2 in data.roles:
            raise HTTPException(status_code=403, detail="Admin cannot create another admin")

    # 🔹 Create user
    new_user = create_user(
        db,
        creator_id=current_user.id,
        name=data.name,
        email=data.email,
        roles=data.roles,
        location=data.location,
        status_id=data.status_id  # 1 = INVITED
    )

    # 🔹 Generate invite token
# 🔹 Generate invite token
    invite_token = create_invite_token(new_user["id"])

    # 🔹 Build invite URL
    # invite_url = f"http://localhost:3000/set-password?token={invite_token}"
    invite_url = f"http://localhost:5173/registration?token={invite_token}"


    # 🔹 Generate email HTML based on role
    html_content = get_invite_email(
        role_id=data.roles[0],  # first role
        name=data.name,
        invite_url=invite_url,
        expiry_hours=24
    )

    # 🔹 Send email
    send_email(
        to_email=data.email,
        subject="PMO Platform Invitation",
        html_content=html_content
    )

    
    # invite_url = f"http://localhost:3000/set-password?token={invite_token}"

    # 🔹 Role objects (frontend friendly)
    roles_data = [{"id": r, "name": f"Role {r}"} for r in data.roles]

    return {
        "success": True,
        "message": "User created successfully. Invitation ready.",
        "data": {
            "user_id": new_user["id"],
            "email": new_user["email"],
            "status": "INVITED",
            "roles": roles_data,
            "invite_url": invite_url,
            "expires_in": 86400  # 24 hours
        }
    }
