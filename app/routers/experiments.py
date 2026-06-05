from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional, List
from app.db.models import (User, Experiment)
from app.schemas.experiment import (ExperimentCreate, ExperimentOut)
from app.services.experiment_service import (fetch_experiment, fetch_all_experiment, fetch_experiment_by_id)
from app.services.project_service import fetch_project_by_id
from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.core.logger import logger
from app.cache.redis_client import redis_client
import json

router = APIRouter(
    prefix="/projects",
    tags=["Experiments"]
)

@router.post("/{projectid}/experiments")
def create_experiment(experiment: ExperimentCreate,projectid: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_experiment = fetch_experiment(db,db_project.projectid)
    if db_experiment:
        raise HTTPException(status_code=400, detail="Experiments with same name exists")
    db_experiment = Experiment(name=experiment.name,params=experiment.params,metrics=experiment.metrics,projectid=projectid)
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    logger.info(f"Experiment {db_experiment.name} created |  ProjectID: {db_experiment.projectid} |   ExperimentID: {db_experiment.experimentid}")
    redis_client.delete(f"experiments:project:{projectid}")
    return {
        "Message":f"Experiment {db_experiment.name} created",
        "ProjectID":db_experiment.projectid,
        "ExperimentID:":db_experiment.experimentid
        }


@router.get("/{projectid}/experiments", response_model=List[ExperimentOut])
def get_experiment(projectid: int, experiment_name: Optional[str] = None, experimentid: Optional[int] = None, sort_by: str = "experimentid",
                 order: str = "asc",  page: int = 1, limit: int = 10, 
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    cache_key = f"experiments:project:{projectid}"
    cached_project =  redis_client.get(cache_key)
    if cached_project:
        logger.info("Cache Hit")
        return json.loads(cached_project) # type: ignore
        
    logger.info("Cache Miss")

    query = fetch_all_experiment(db, projectid)

    allowed_sort_fields = ["experimentid", "name"]
    allowed_orders = ["asc", "desc"]

    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400,detail="Invalid option for Sort_by, Sort_by should be experimentid or name")
    if order not in allowed_orders:
        raise HTTPException(status_code=400,detail="Invalid option for Order, Order should be asc or desc")    
    if  page < 1:
        raise HTTPException(status_code=400,detail="Page should be 1 or greater")
    if  limit >100:
        raise HTTPException(status_code=400,detail="limit should be 100 or less")


    if experiment_name:
        query = query.filter(Experiment.name == experiment_name) 
    if experimentid:
        query = query.filter(Experiment.experimentid == experimentid)

    column = getattr(Experiment, sort_by)
    query = query.order_by(asc(column) if order == "asc" else desc(column))
    
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    experiments = query.all()
    json_experiments= []
    for experiment in experiments:
        data = ExperimentOut.model_validate(experiment)
        json_experiments.append(data.model_dump())
    redis_client.set(
    cache_key,
    json.dumps(json_experiments),
    ex=300
    )
    return experiments


@router.get("/{projectid}/experiments/{experimentid}", response_model=List[ExperimentOut])
def get_experiment_by_id(projectid: int,experimentid: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_experiment = fetch_experiment_by_id(db,db_project.projectid,experimentid)
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiments not found")
    return db_experiment

@router.delete("/{projectid}/experiments/{experimentid}")
def delete_experiment_by_id(projectid: int,experimentid:int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_experiment = fetch_experiment_by_id(db,db_project.projectid,experimentid)
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiments not found")
    db.delete(db_experiment)
    db.commit()
    logger.info(f"Experiment {db_experiment.name} deleted for user {current_user.username}")
    redis_client.delete(f"experiments:project:{projectid}")
    return {"Message": f"Experiment {db_experiment.name} deleted for user {current_user.username}"}

