from sqlalchemy.orm import Session
from app.db.models import Project

def fetch_project(db: Session, project_name: str, userid):
    return db.query(Project).filter(Project.name == project_name ,Project.userid ==userid).first()

def fetch_all_project(db: Session, userid):
    return db.query(Project).filter(Project.userid ==userid).all()

def fetch_project_by_id(db: Session, project_id, userid):
    return db.query(Project).filter(Project.projectid== project_id ,Project.userid ==userid).first()
