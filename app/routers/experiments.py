from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.models import (User, Experiment)
from app.schemas.experiment import (ExperimentCreate, ExperimentOut)
from app.services.experiment_service import (fetch_experiment, fetch_experiment_by_id)
from app.services.project_service import (fetch_project, fetch_all_project, fetch_project_by_id)
from app.dependencies.auth import (get_current_user)
from app.db.database import get_db

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
    return {
        "Message":f"Experiment {db_experiment.name} created",
        "ProjectID":db_experiment.projectid,
        "ExperimentID:":db_experiment.experimentid
        }


@router.get("/{projectid}/experiments")
def get_experiments_all(projectid: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    db_project = fetch_project_by_id(db,projectid,current_user.userid)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_experiment = fetch_experiment(db,db_project.projectid)
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiments not found")
    return db_experiment


@router.get("/{projectid}/experiments/{experimentid}")
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
    return {"Message": f"Project {db_experiment.name} deleted for user {current_user.username}."}

