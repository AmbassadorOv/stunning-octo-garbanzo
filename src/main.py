from fastapi import FastAPI
from .app import orchestrator, remote

app = FastAPI()

app.include_router(orchestrator.router)
app.include_router(remote.router)
