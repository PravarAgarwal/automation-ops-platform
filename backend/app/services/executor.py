import subprocess
from subprocess import TimeoutExpired
from datetime import datetime
from sqlalchemy.orm import Session
from app import models
from app.config import logger

def execute_job(execution_id: int, db: Session):
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
            raise ValueError("Unsupported script type")

        MAX_OUTPUT_SIZE = 10_000

        execution.stdout = (
            result.stdout[:MAX_OUTPUT_SIZE] if result.stdout else None
        )
        execution.stderr = (
            result.stderr[:MAX_OUTPUT_SIZE] if result.stderr else None
        )
        execution.exit_code = result.returncode
        execution.finished_at = datetime.utcnow()

        if result.returncode == 0:
            execution.status = models.ExecutionStatus.SUCCESS
            logger.info(f"Execution {execution_id} succeeded")
        else:
            execution.status = models.ExecutionStatus.FAILED
            logger.error(
                f"Execution {execution_id} failed with exit_code={result.returncode}"
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
