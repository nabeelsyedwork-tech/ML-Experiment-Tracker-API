from pydantic import BaseModel

class ExperimentCreate(BaseModel):
    name: str
    params: dict
    metrics: dict

class ExperimentOut(BaseModel):
    name: str
    experimentid: int
    projectid: int
    params: dict
    metrics: dict