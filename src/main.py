from fastapi import FastAPI
from .app import orchestrator

app = FastAPI()

app.include_router(orchestrator.router)
