from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.models.client import Client
from app.models.project_status import ProjectStatus
from datetime import datetime

def create_project(db: Session, project_data, created_by: int):

    # ✅ check client by email
    client = db.query(Client).filter(Client.email == project_data.client_email).first()
    if not client:
        raise HTTPException(
            status_code=404,
            detail="No client registration with this email"
        )

    # ✅ check status
    status = db.query(ProjectStatus).filter(ProjectStatus.id == project_data.status_id).first()
    if not status:
        raise HTTPException(status_code=400, detail="Invalid project status")

    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        client_id=client.id,
        location=project_data.location,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        status_id=project_data.status_id,
        created_by=created_by,
        created_at=datetime.utcnow()
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "id": new_project.id,
        "name": new_project.name,
        "client": client.email,
        "status": status.name
    }


def get_employees_only(db: Session):
    return db.query(User).filter(User.role == "employee").all()


def invite_employees(db: Session, project_id: int, employee_ids):
    members = []
    for emp_id in employee_ids:
        member = ProjectMember(
            project_id=project_id,
            user_id=emp_id,
            role="employee"
        )
        db.add(member)
        members.append(member)

    db.commit()
    return members
