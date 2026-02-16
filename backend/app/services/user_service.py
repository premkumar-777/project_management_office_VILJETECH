# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.models.user_role import UserRole
# from app.models.client import Client
# from app.core.security import create_temp_token


# def create_user(
#     db: Session,
#     creator_id: int,
#     name: str,
#     email: str,
#     roles: list,
#     location: str,
#     status_id: int = 1,
# ):
#     """
#     Creates a user or assigns roles if user already exists.
#     Role 5 = client → stored in clients table.
#     """

#     is_client = 5 in roles

#     # ================= CLIENT FLOW =================
#     if is_client:
#         existing_client = db.query(Client).filter(Client.email == email).first()

#         if existing_client:
#             temp_token = create_temp_token(existing_client.id)
#             return {
#                 "id": existing_client.id,
#                 "email": existing_client.email,
#                 "message": "Client already exists",
#                 "temp_token": temp_token,
#             }

#         client = Client(
#             name=name,
#             email=email,
#             location=location,
#             status_id=status_id,
#             created_by=creator_id,
#             mfa_enabled=0,
#         )
#         db.add(client)
#         db.commit()
#         db.refresh(client)

#         temp_token = create_temp_token(client.id)

#         return {
#             "id": client.id,
#             "email": client.email,
#             "temp_token": temp_token,
#         }

#     # ================= USER FLOW =================
#     user = db.query(User).filter(User.email == email).first()

#     # 🔹 If user DOES NOT exist → create
#     if not user:
#         user = User(
#             name=name,
#             email=email,
#             location=location,
#             status_id=status_id,
#             created_by=creator_id,
#         )
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     # 🔹 Assign roles (avoid duplicates)
#     existing_roles = (
#         db.query(UserRole.role_id)
#         .filter(UserRole.user_id == user.id)
#         .all()
#     )
#     existing_role_ids = {r[0] for r in existing_roles}

#     for role_id in roles:
#         if role_id not in existing_role_ids:
#             db.add(
#                 UserRole(
#                     user_id=user.id,
#                     role_id=role_id,
#                     assigned_by=creator_id,
#                 )
#             )

#     db.commit()

#     temp_token = create_temp_token(user.id)

#     return {
#         "id": user.id,
#         "email": user.email,
#         "temp_token": temp_token,
#     }

from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_role import UserRole
from app.models.client import Client
from app.core.security import create_temp_token


def create_user(
    db: Session,
    creator_id: int,
    name: str,
    email: str,
    roles: list,
    location: str,
    status_id: int = 1,
):
    """
    Creates a user or assigns roles if user already exists.
    Role 5 = client → stored in clients table.
    """

    is_client = 5 in roles

    # ================= CLIENT FLOW =================
    if is_client:
        existing_client = db.query(Client).filter(Client.email == email).first()

        if existing_client:
            temp_token = create_temp_token(existing_client.id)
            return {
                "id": existing_client.id,
                "email": existing_client.email,
                "message": "Client already exists",
                "temp_token": temp_token,
            }

        client = Client(
            name=name,
            email=email,
            location=location,
            status_id=status_id,
            created_by=creator_id,
            mfa_enabled=0,
        )
        db.add(client)
        db.commit()
        db.refresh(client)

        temp_token = create_temp_token(client.id)

        return {
            "id": client.id,
            "email": client.email,
            "temp_token": temp_token,
        }

    # ================= USER FLOW =================
    user = db.query(User).filter(User.email == email).first()

    # 🔹 If user DOES NOT exist → create
    if not user:
        user = User(
            name=name,
            email=email,
            location=location,
            status_id=status_id,
            created_by=creator_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 🔹 Assign roles (avoid duplicates)
    existing_roles = (
        db.query(UserRole.role_id)
        .filter(UserRole.user_id == user.id)
        .all()
    )
    existing_role_ids = {r[0] for r in existing_roles}

    for role_id in roles:
        if role_id not in existing_role_ids:
            db.add(
                UserRole(
                    user_id=user.id,
                    role_id=role_id,
                    assigned_by=creator_id,
                )
            )

    db.commit()

    temp_token = create_temp_token(user.id)

    return {
        "id": user.id,
        "email": user.email,
        "temp_token": temp_token,
    }
