from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import models, schemas # Classes created by me for the database and Pydantic schemas
from app.database import SessionLocal, get_db

from typing import List
from app.services.executor import execute_job

'''
APIRouter → group endpoints
Session → DB session type
models → DB tables
schemas → input/output validation
'''

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)

@router.post("/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(name=job.name, 
                        script_type=job.script_type,
                        script_content=job.script_content)
    db.add(db_job)
    db.commit()
    # at this point (db.refresh(db_job)), db_job gets its ID from the DB
    db.refresh(db_job)
    return db_job

@router.post("/{job_id}/run")
def run_job(job_id: int, background_tasks : BackgroundTasks, db : Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    existing_execution = (
        db.query(models.JobExecution)
        .filter(
            models.JobExecution.job_id == job.id,
            models.JobExecution.status == models.ExecutionStatus.RUNNING,
        )
        .first()
    )
    if existing_execution:
        raise HTTPException(status_code=409, detail="Job is already running")

    execution = models.JobExecution(
        job_id=job.id,
        status=models.ExecutionStatus.PENDING,
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    background_tasks.add_task(execute_job, execution.id)

    return {"execution_id": execution.id, 
            "status": execution.status}

@router.get("/", response_model=List[schemas.JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs

@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/by_name/{job_name}", response_model=schemas.JobResponse)
def get_job_by_name(job_name: str, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.name == job_name).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/by_script_type/{script_type}", response_model=List[schemas.JobResponse])
def get_jobs_by_script_type(script_type: str, db: Session = Depends(get_db)):
    jobs = db.query(models.Job).filter(models.Job.script_type == script_type).all()
    return jobs

@router.patch("/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job_update.name is not None:
        job.name = job_update.name
    if job_update.script_type is not None:
        job.script_type = job_update.script_type
    if job_update.script_content is not None:
        job.script_content = job_update.script_content
    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", response_model=schemas.JobResponse)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return job

