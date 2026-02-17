# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from app.models.project import Project
# from app.models.project_member import ProjectMember
# from app.models.user import User
# from app.models.client import Client
# from app.models.project_status import ProjectStatus
# from datetime import datetime

# def create_project(db: Session, project_data, created_by: int):

#     # ✅ check client by email
#     client = db.query(Client).filter(Client.email == project_data.client_email).first()
#     if not client:
#         raise HTTPException(
#             status_code=404,
#             detail="No client registration with this email"
#         )

#     # ✅ check status
#     status = db.query(ProjectStatus).filter(ProjectStatus.id == project_data.status_id).first()
#     if not status:
#         raise HTTPException(status_code=400, detail="Invalid project status")

#     new_project = Project(
#         name=project_data.name,
#         description=project_data.description,
#         client_id=client.id,
#         location=project_data.location,
#         start_date=project_data.start_date,
#         end_date=project_data.end_date,
#         status_id=project_data.status_id,
#         created_by=created_by,
#         created_at=datetime.utcnow()
#     )

#     db.add(new_project)
#     db.commit()
#     db.refresh(new_project)

#     return {
#         "id": new_project.id,
#         "name": new_project.name,
#         "client": client.email,
#         "status": status.name
#     }


# def assign_project_members(db, project_id, user_ids, role_id, assigned_by):

#     project = db.query(Project).filter(Project.id == project_id).first()
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")

#     assigned_members = []

#     for user_id in user_ids:

#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             continue

#         member = ProjectMember(
#             project_id=project_id,
#             user_id=user_id,
#             role_id=role_id,
#             assigned_by=assigned_by,
            
#         )

#         db.add(member)
#         assigned_members.append(user.email)

#     db.commit()

#     return {
#         "project_id": project_id,
#         "assigned_users": assigned_members
#     }

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.project import Project
from app.models.client import Client
from app.models.project_member import ProjectMember
from app.models.user import User
from app.models.user_role import UserRole


# ---------------------------------------------------
# CREATE PROJECT (Admin)
# ---------------------------------------------------
def create_project(db: Session, data, current_user):

    # ✅ check client by email
    client = db.query(Client).filter(Client.email == data.client_email).first()
    if not client:
        raise HTTPException(
            status_code=404,
            detail="No client registered with this email"
        )

    project = Project(
        name=data.name,
        description=data.description,
        location=data.location,
        start_date=data.start_date,
        end_date=data.end_date,
        status_id=data.status_id,
        client_id=client.id,
        created_by=current_user.id,
        created_at=datetime.utcnow()
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project created successfully",
        "project_id": project.id
    }


# ---------------------------------------------------
# GET ALL PROJECTS (Admin)
# ---------------------------------------------------
def get_all_projects(db: Session):

    projects = db.query(Project).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "status_id": p.status_id,
            "client_id": p.client_id,
            "start_date": p.start_date,
            "end_date": p.end_date
        }
        for p in projects
    ]


# ---------------------------------------------------
# GET MY PROJECTS (Manager / Employee)
# ---------------------------------------------------
def get_my_projects(db: Session, user_id: int):

    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == user_id
    ).all()

    project_ids = [m.project_id for m in memberships]

    projects = db.query(Project).filter(Project.id.in_(project_ids)).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "status_id": p.status_id
        }
        for p in projects
    ]


# ---------------------------------------------------
# ASSIGN MEMBERS TO PROJECT
# Only Project Manager (role_id=3)
# and Employee (role_id=4)
# ---------------------------------------------------
def assign_members(db: Session, project_id: int, members, current_user):

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    added_members = []

    for m in members:

        user = db.query(User).filter(User.id == m.user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User {m.user_id} not found"
            )

        # ✅ check role
        role = db.query(UserRole).filter(
            UserRole.user_id == m.user_id,
            UserRole.role_id.in_([3, 4])  # PM or Employee
        ).first()

        if not role:
            raise HTTPException(
                status_code=400,
                detail=f"User {m.user_id} is not PM or Employee"
            )

        member = ProjectMember(
            project_id=project_id,
            user_id=m.user_id,
            role_id=m.role_id
        )

        db.add(member)
        added_members.append(m.user_id)

    db.commit()

    return {
        "message": "Members assigned successfully",
        "members": added_members
    }


# ---------------------------------------------------
# GET PROJECT MEMBERS
# ---------------------------------------------------
def get_project_members(db: Session, project_id: int):

    members = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).all()

    result = []

    for m in members:
        result.append({
            "user_id": m.user_id,
            "role_id": m.role_id
        })

    return result
