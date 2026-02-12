# # app/services/user_service.py
# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.models.user_role import UserRole

# def create_user(db: Session, creator_id: int, name: str, email: str, roles: list, location: str, status_id: int = 1):
#     """
#     Creates a user without password and assigns roles using ORM.
#     """
#     # 1️⃣ Create user
#     user = User(
#         name=name,
#         email=email,
#         location=location,
#         status_id=status_id,
#         created_by=creator_id
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)  # load generated id

#     # 2️⃣ Assign roles
#     for role_id in roles:
#         user_role = UserRole(
#             user_id=user.id,
#             role_id=role_id,
#             assigned_by=creator_id
#         )
#         db.add(user_role)

#     db.commit()
#     return {"id": user.id, "email": user.email}
# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_role import UserRole
from app.models.client import Client
from app.core.security import create_temp_token

def create_user(db: Session, creator_id: int, name: str, email: str, roles: list, location: str, status_id: int = 1):
    """
    Creates a user or client.
    Role 5 = client → store in clients table with MFA support.
    """
    is_client = 5 in roles  # 5 = client

    if is_client:
        # 🔹 Create client in clients table
        client = Client(
            name=name,
            email=email,
            location=location,
            status_id=status_id,
            created_by=creator_id,
            mfa_enabled=0  # default MFA disabled
        )
        db.add(client)
        db.commit()
        db.refresh(client)

        # 🔹 Generate temp token for first-time login
        temp_token = create_temp_token(client.id)

        return {
            "id": client.id,
            "email": client.email,
            "temp_token": temp_token
        }

    else:
        # 🔹 Create regular user
        user = User(
            name=name,
            email=email,
            location=location,
            status_id=status_id,
            created_by=creator_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 🔹 Assign roles
        from app.models.user_role import UserRole
        for role_id in roles:
            user_role = UserRole(
                user_id=user.id,
                role_id=role_id,
                assigned_by=creator_id
            )
            db.add(user_role)
        db.commit()

        temp_token = create_temp_token(user.id)

        return {
            "id": user.id,
            "email": user.email,
            "temp_token": temp_token
        }
