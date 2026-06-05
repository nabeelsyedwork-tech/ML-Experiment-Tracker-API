from pydantic import BaseModel, ConfigDict

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    name: str
    projectid: int
    userid: int
    class Config:
        from_attributes = True
    
