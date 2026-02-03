import subprocess
from subprocess import TimeoutExpired
from datetime import datetime
from sqlalchemy.orm import Session
from app import models
from app.config import logger
from app.database import SessionLocal

MAX_OUTPUT_SIZE = 10_000
EXECUTION_TIMEOUT_SECONDS = 10

def _mark_failed(db, execution, message:str):
    execution.status = models.ExecutionStatus.FAILED
    execution.stderr = message[:MAX_OUTPUT_SIZE]
    execution.finished_at = datetime.utcnow()
    db.commit()

def execute_job(execution_id: int):
    # creating private db instance for the background task
    db = SessionLocal()
    execution = None

    try:
        execution = (
            db.query(models.JobExecution)
            .filter(models.JobExecution.id == execution_id)
            .first()
        )

        if execution is None:
            logger.warning(f"Execution {execution_id} not found")
            return

        if execution.status != models.ExecutionStatus.PENDING:
            logger.warning(
                f"Execution {execution_id} is not in PENDING state"
            )
            return

        job = execution.job

        logger.info(f"Starting execution_id={execution_id}")
        logger.info(f"Job type={job.script_type}")

        execution.status = models.ExecutionStatus.RUNNING
        db.commit()

        if job.script_type == "python":
            result = subprocess.run(
                ["python", "-c", job.script_content],
                capture_output=True,
                text=True,
                timeout=10,
            )
        elif job.script_type == "bash":
            result = subprocess.run(
                ["bash", "-c", job.script_content],
                capture_output=True,
                text=True,
                timeout=10,
            )
        else:
            _mark_failed(db, execution, "Unsupported script type")

        execution.stdout = (
            result.stdout[:MAX_OUTPUT_SIZE] if result.stdout else None
        )
        execution.stderr = (
            result.stderr[:MAX_OUTPUT_SIZE] if result.stderr else None
        )
        execution.exit_code = result.returncode
        execution.finished_at = datetime.utcnow()

        execution.status = (
            models.ExecutionStatus.SUCCESS
            if result.returncode == 0
            else models.ExecutionStatus.FAILED
        )

        db.commit()

    except TimeoutExpired:
        execution.status = models.ExecutionStatus.FAILED
        execution.stderr = "Execution timed out"
        execution.finished_at = datetime.utcnow()
        db.commit()

        logger.error(f"Execution {execution_id} timed out")

    except Exception as e:
        execution.status = models.ExecutionStatus.FAILED
        execution.stderr = str(e)
        execution.finished_at = datetime.utcnow()
        db.commit()

        logger.exception(
            f"Unhandled exception during execution {execution_id}"
        )

    finally:
        db.close()
