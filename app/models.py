# all the database table definitions and ORM models

'''
Docstring for app.models
This file answers:

“What data do we store permanently?”

Each class here:

Maps to one database table

Defines:
Columns
Types
Primary keys

Example mentally:
Job
Execution
User

Think of this as:
“Schema definition for persistent state”
Very similar to defining CSV structure — but permanent.
'''


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum
from datetime import datetime

class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    script_type = Column(String, index=True)

    executions = relationship("JobExecution", back_populates="job", cascade="all, delete-orphan")

class JobExecution(Base):
    __tablename__ = "job_executions"
    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False) # jobs is the __tablename__ for Job class 

    status = Column(String, nullable=False, default=ExecutionStatus.PENDING)

    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    job = relationship("Job", back_populates="executions")
