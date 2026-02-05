'''
Docstring for app.main
This is the starting point of the backend.

Analogy:

In scripts → if __name__ == "__main__"
Here → main.py

What it does:
Creates the FastAPI application
Registers routers (endpoints)

Initializes the database
It should:
Be small
Be boring

Contain no business logic
If main.py grows large → structure is broken.
'''

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models
from app.routers import jobs, health, executions


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ runs once, before receiving requests
    # create all tables, tables should be created at the start of the code, so this line is here.
    Base.metadata.create_all(bind=engine)
    yield
    # ✅ runs once, on shutdown (optional cleanup)
    # (Nothing to close for SQLAlchemy engine in this simple setup)

app = FastAPI(title="Automation Ops Platform", lifespan=lifespan)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"],
)

app.include_router(jobs.router)
app.include_router(health.router)
app.include_router(executions.router)