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


from sqlalchemy import Column, Integer, String
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    script_type = Column(String, index=True)


