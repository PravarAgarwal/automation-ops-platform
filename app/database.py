# all the database connection and session management logic

'''
Docstring for app.database
This file answers:

“How does the app talk to the database?”

It contains:

Database URL
Connection setup
Session creation

Analogy to scripting:
Like setting up a file handle once
Then reusing it everywhere

Why separate file?
DB config changes often
You don’t want DB logic scattered across files
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_URL

# creating db engine, through this FastAPI talks to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# creating session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# base class for all models (tables)
# it is used to create models by inheriting from it, so that SQLAlchemy knows these are models
# Without this, SQLAlchemy wouldn’t know how to connect Python class to the database schema.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()