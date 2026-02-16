from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.project_schema import ProjectCreate, ProjectResponse, InviteEmployees
from app.services.project_service import create_project, get_employees_only, invite_employees
from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.user_role import UserRole
from app.models.role import Role
router = APIRouter(prefix="/projects", tags=["Projects"])


# ✅ Only Admin can create project
@router.post("/")
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_roles = [ur.role.role.lower() for ur in current_user.roles]

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Only admin can create projects")


    new_project = create_project(db, project, current_user.id)

    return {
        "success": True,
        "message": "Project created successfully",
        "data": new_project
    }



# ✅ Get employees list (for invite dropdown)
@router.get("/employees")
def employees_list(db: Session = Depends(get_db)):
    employees = get_employees_only(db)

    return {
        "success": True,
        "message": "Employees fetched successfully",
        "data": employees
    }



# ✅ Project manager invite employees
@router.post("/{project_id}/invite")
def invite_project_members(
    project_id: int,
    data: InviteEmployees,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "project_manager":
        raise HTTPException(status_code=403, detail="Only project manager can invite")

    members = invite_employees(db, project_id, data.employee_ids)

    return {
        "success": True,
        "message": "Employees invited successfully",
        "data": members
    }

