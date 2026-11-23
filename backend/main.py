
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import health, research, history, sessions
from database.database import init_db

app = FastAPI(
    title="AI Research Assistant API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(research.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    init_db()
