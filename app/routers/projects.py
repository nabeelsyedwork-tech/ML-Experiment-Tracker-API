from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import (User, Project)
from app.schemas.project import (ProjectCreate, ProjectOut)
from app.services.project_service import (fetch_project, fetch_all_project, fetch_project_by_id)
from app.dependencies.auth import (get_current_user)


router = APIRouter(
    prefix="/projects",
    tags=["Project"]
)

@router.post("")
def create_project(project:ProjectCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project(db,project_name=project.name,userid=current_user.userid)
    if db_project:
        raise HTTPException(status_code=400, detail="Project with same name exists")
    db_project = Project(name=project.name,userid=current_user.userid)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return {
        "Message":f"Project {project.name} created",
        "ProjectID":db_project.projectid,
        "UserID":db_project.userid      
    }
@router.get("")
def get_projects_all(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_all_project(db,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.get("/{projectid}")
def get_project_by_id(projectid: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{projectid}")
def delete_project_by_id(projectid: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"Message": f"Project {db_project.name} deleted for user {current_user.username}."}