from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional, List
from app.db.database import get_db
from app.db.models import (User, Project)
from app.schemas.project import (ProjectCreate, ProjectOut)
from app.services.project_service import (fetch_project, fetch_all_project, fetch_project_by_id)
from app.dependencies.auth import (get_current_user)
from app.core.logger import logger
import json
from app.cache.redis_client import redis_client

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
    logger.info(f"Project {project.name} created |  ProjectID: {db_project.projectid} |  UserID: {db_project.userid}")
    redis_client.delete(f"projects:user:{current_user.userid}")
    return {
        "Message":f"Project {project.name} created",
        "ProjectID":db_project.projectid,
        "UserID":db_project.userid      
    }
@router.get("",response_model=List[ProjectOut])
def get_projects(project_name: Optional[str] = None, projectid: Optional[int] = None, sort_by: str = "projectid",
                 order: str = "asc",  page: int = 1, limit: int = 10, 
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cache_key = f"projects:user:{current_user.userid}"
    cached_project =  redis_client.get(cache_key)
    if cached_project:
        logger.info("Cache Hit")
        return json.loads(cached_project) # type: ignore
        
    logger.info("Cache Miss")
    query = fetch_all_project(db, current_user.userid)

    allowed_sort_fields = ["projectid", "name"]
    allowed_orders = ["asc", "desc"]

    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400,detail="Invalid option for Sort_by, Sort_by should be projectid or name")
    if order not in allowed_orders:
        raise HTTPException(status_code=400,detail="Invalid option for Order, Order should be asc or desc")    
    if  page < 1:
        raise HTTPException(status_code=400,detail="Page should be 1 or greater")
    if  limit >100:
        raise HTTPException(status_code=400,detail="limit should be 100 or less")


    if project_name:
        query = query.filter(Project.name == project_name)
    if projectid:
        query = query.filter(Project.projectid == projectid)

    column = getattr(Project, sort_by)
    query = query.order_by(asc(column) if order == "asc" else desc(column))
    
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    projects = query.all()
    json_projects = []
    for project in projects:
        data = ProjectOut.model_validate(project)
        json_projects.append(data.model_dump())
    redis_client.set(
    cache_key,
    json.dumps(json_projects),
    ex=300
    )
    return projects

@router.get("/{projectid}",response_model=List[ProjectOut])
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
    logger.info(f"Project {db_project.name} deleted for user {current_user.username}")
    redis_client.delete(f"projects:user:{current_user.userid}")
    return {"Message": f"Project {db_project.name} deleted for user {current_user.username}"}