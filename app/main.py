from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.projects import router as project_router
from app.routers.experiments import router as experiment_router
from app.core.logger import logger
from app.db.database import Base, engine, session_local
app = FastAPI(
    title="ML Experiment Tracker"
)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(experiment_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up.")
    Base.metadata.create_all(bind=engine)
    db = session_local()
    db.close()

@app.get("/")
def root():
    return {
        "Message": "ML Experiment Tracker"
    }

