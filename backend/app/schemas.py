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
from app.models import ExecutionStatus

class ScriptType(str, Enum):
    python = "python"
    bash = "bash"

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
    script_content: str

class JobUpdate(BaseModel):
    name: Optional[str] = None
    script_type: Optional[ScriptType] = None
    script_content: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    name: str
    script_type: ScriptType
    script_content: str

    # this tells pydantic that the data might come from a SQLAlchemy model
    class Config:
        from_attributes = True

