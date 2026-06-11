from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.models.project import Project
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Logistics Showcases"])

@router.get("", response_model=List[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    """
    Get all active logistics highlight projects / cases. Open to public.
    """
    return db.query(Project).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get granular details about a specific logistical project showcase. Open to public.
    """
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Logistics project showcase item does not exist."
        )
    return db_project

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Create a new logistics project showcase item (Administrator privilege required).
    """
    db_project = Project(
        title=project_in.title,
        category=project_in.category,
        tag=project_in.tag,
        description=project_in.description,
        image_url=project_in.image_url
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
