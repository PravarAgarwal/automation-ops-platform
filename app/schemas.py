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

class JobCreate(BaseModel):
    name: str
    script_type: str

class JobResponse(BaseModel):
    id: int
    name: str
    script_type: str

    # this tells pydantic that the data might come from a SQLAlchemy model
    class Config:
        from_attributes = True

