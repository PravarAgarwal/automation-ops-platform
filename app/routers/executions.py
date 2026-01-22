from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app import models, schemas

from app.services.executor import execute_job

router = APIRouter(
    prefix="/executions", tags=["executions"]
)

@router.get("/{execution_id}", response_model=schemas.JobExecutionResponse)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    execution = db.query(models.JobExecution).filter(models.JobExecution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution

@router.post("/{job_id}/run")
def run_job(job_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    execution = models.JobExecution(
        job_id=job.id,
        status=models.ExecutionStatus.PENDING,
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    background_tasks.add_task(execute_job, execution.id, SessionLocal())

    return {
        "execution_id": execution.id,
        "status": execution.status,
    }