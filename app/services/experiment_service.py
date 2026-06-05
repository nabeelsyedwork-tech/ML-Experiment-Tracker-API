from sqlalchemy.orm import Session
from app.db.models import Experiment

def fetch_experiment(db: Session, project_id):
    return db.query(Experiment).filter(Experiment.projectid == project_id).first()

def fetch_all_experiment(db: Session, project_id):
    return db.query(Experiment).filter(Experiment.projectid == project_id)

def fetch_experiment_by_id(db:Session, project_id, experiment_id):
    return db.query(Experiment).filter(Experiment.projectid == project_id ,Experiment.experimentid == experiment_id).first()
