from fastapi import FastAPI
from .app import orchestrator
from .app import lamina

app = FastAPI()

app.include_router(lamina.router)
app.include_router(orchestrator.router)
