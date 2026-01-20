# What data is allowed to come in or go out through APIs?
'''
Docstring for app.schemas
This file answers:

“Where do settings live?”

Examples:
DB URL
Secret keys
Environment variables

Why separate?
Different environments:
Local
Test
Production
You never hardcode secrets.
'''

from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class ScriptType(str, Enum):
    python = "python"
    bash = "bash"

class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class JobExecutionResponse(BaseModel):
    id: int
    job_id: int
    status: ExecutionStatus
    stdout: Optional[str]
    stderr: Optional[str]
    exit_code: Optional[int]
    created_at: datetime
    finished_at: Optional[datetime]

    # this tells pydantic that the data might come from a SQLAlchemy model
    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    name: str
    script_type: ScriptType

class JobUpdate(BaseModel):
    name: Optional[str] = None
    script_type: Optional[ScriptType] = None

class JobResponse(BaseModel):
    id: int
    name: str
    script_type: ScriptType

    # this tells pydantic that the data might come from a SQLAlchemy model
    class Config:
        from_attributes = True

