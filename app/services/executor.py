import subprocess
from subprocess import TimeoutExpired
from datetime import datetime
from sqlalchemy.orm import Session
from app import models

def execute_job(execution_id: int, db: Session):
    execution = (
        db.query(models.JobExecution)
        .filter(models.JobExecution.id == execution_id)
        .first()
    )

    if execution is None:
        return

    job = execution.job

    print("Executing job:", execution_id)
    print("Script content:", job.script_content)

    execution.status = models.ExecutionStatus.RUNNING
    db.commit()

    try:
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

        print("Return code:", result.returncode)
        print("STDOUT:", repr(result.stdout))
        print("STDERR:", repr(result.stderr))

        MAX_OUTPUT_SIZE = 10_000  # characters

        execution.stdout = result.stdout[:MAX_OUTPUT_SIZE]
        execution.stderr = result.stderr[:MAX_OUTPUT_SIZE]
        execution.exit_code = result.returncode
        execution.finished_at = datetime.utcnow()

        if result.returncode == 0:
            execution.status = models.ExecutionStatus.SUCCESS
        else:
            execution.status = models.ExecutionStatus.FAILED

    except TimeoutExpired as e:
        execution.stderr = "Execution timed out"
        execution.status = models.ExecutionStatus.FAILED
        execution.finished_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        execution.stderr = str(e)
        execution.status = models.ExecutionStatus.FAILED
        execution.finished_at = datetime.utcnow()

    finally:
        if execution.finished_at is None:
            execution.finished_at = datetime.utcnow()
            db.commit()
            db.close()

    db.commit()
