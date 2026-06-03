from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.projects import router as project_router
from app.routers.experiments import router as experiment_router

app = FastAPI(
    title="ML Experiment Tracker"
)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(experiment_router)

@app.get("/")
def root():
    return {
        "Message": "ML Experiment Tracker"
    }