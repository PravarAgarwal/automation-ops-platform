from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app import models, schemas

from app.services.executor import execute_job

from typing import List

router = APIRouter(
    prefix="/executions", tags=["executions"]
)

@router.get("/{execution_id}", response_model=schemas.JobExecutionResponse)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    execution = db.query(models.JobExecution).filter(models.JobExecution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution

@router.get("/job/{job_id}", response_model=List[schemas.JobExecutionResponse])
def get_job_executions(job_id: int, db: Session = Depends(get_db)):
    executions = db.query(models.JobExecution).filter(models.JobExecution.job_id == job_id).all()
    return executions