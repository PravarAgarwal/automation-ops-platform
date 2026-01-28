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

from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routers import jobs, health, executions

# create all tables, tables should be created at the start of the code, so this line is here.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automation Ops Platform")

app.include_router(jobs.router)
app.include_router(health.router)
app.include_router(executions.router)