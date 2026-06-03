from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    name: str
    projectid: int
    userid: int
