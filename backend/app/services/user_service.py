# app/services/user_service.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.sql import queries
import secrets

def create_user(db: Session, creator_id: int, name: str, email: str, roles: list, location: str, status_id: int = 1):
    """
    Creates a user without password, assigns roles.
    """
    conn = db.connection()

    # Insert into users table
    result = conn.execute(
        text(queries.INSERT_USER),
        {
            "name": name,
            "email": email,
            "location": location,
            "status_id": status_id,
            "created_by": creator_id
        }
    )
    db.commit()
    user_id = result.lastrowid

    # Insert roles
    for role_id in roles:
        conn.execute(
            text(queries.INSERT_USER_ROLE),
            {
                "user_id": user_id,
                "role_id": role_id,
                "assigned_by": creator_id
            }
        )
    db.commit()
    return {"id": user_id, "email": email}
