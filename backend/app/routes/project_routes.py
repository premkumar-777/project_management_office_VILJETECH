from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project_schema import ProjectCreate, AssignMembersRequest
from app.services.project_service import (
    create_project,
    get_all_projects,
    get_my_projects,
    assign_members,
    get_project_members
)
from app.core.auth_dependency import get_current_user


router = APIRouter(prefix="/projects", tags=["Projects"])


# --------------------------------------------------
# CREATE PROJECT (Admin)
# --------------------------------------------------
@router.post("/")
def create_project_api(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_project(db, data, current_user)


# --------------------------------------------------
# GET ALL PROJECTS
# --------------------------------------------------
@router.get("/")
def get_projects_api(
    db: Session = Depends(get_db),
):
    return get_all_projects(db)


# --------------------------------------------------
# GET MY PROJECTS
# --------------------------------------------------
@router.get("/my")
def get_my_projects_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_my_projects(db, current_user.id)


# --------------------------------------------------
# ASSIGN MEMBERS
# --------------------------------------------------
@router.post("/{project_id}/assign")
def assign_members_api(
    project_id: int,
    request: AssignMembersRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return assign_members(db, project_id, request.members, current_user)


# --------------------------------------------------
# GET PROJECT MEMBERS
# --------------------------------------------------
@router.get("/{project_id}/members")
def get_project_members_api(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_project_members(db, project_id)
