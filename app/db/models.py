from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'
    userid = Column(Integer, index=True, primary_key=True, autoincrement=True)
    username = Column(String,unique=True, index=True)
    password = Column(String)
    projects = relationship('Project', back_populates='user')

class Project(Base):
    __tablename__ = 'projects'
    projectid = Column(Integer, index=True, primary_key=True,autoincrement=True)
    name = Column(String)
    userid = Column(Integer, ForeignKey("users.userid"))
    user = relationship('User',back_populates='projects')
    experiments = relationship("Experiment", back_populates="project")

class Experiment(Base):
    __tablename__ = 'experiments'
    name = Column(String)
    experimentid = Column(Integer, primary_key=True,index=True,autoincrement=True)
    params = Column(JSON)
    metrics = Column(JSON)
    projectid = Column(Integer, ForeignKey('projects.projectid'))
    project = relationship('Project', back_populates='experiments')
