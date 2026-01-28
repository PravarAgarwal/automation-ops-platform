# 🛠 Automation Job Execution Platform

A backend service to **store, execute, and track automation scripts asynchronously**, with execution safety, status tracking, and log capture.

This project simulates an internal automation platform commonly used in trading firms, DevOps teams, or data engineering workflows.

---

## 🚀 Features

- Create automation jobs (Python / Bash)
- Execute jobs asynchronously (non-blocking API)
- Track execution lifecycle:
  - `PENDING → RUNNING → SUCCESS / FAILED`
- Capture:
  - `stdout`
  - `stderr`
  - exit codes
- Protect the system from:
  - Infinite loops (execution timeouts)
  - Long-running scripts
- Clean, modular project structure
- OpenAPI documentation via FastAPI

---

## 🧠 Why This Project?

Many internal systems need to run scripts **without blocking APIs**, while still:

- Knowing execution status
- Capturing logs
- Handling failures safely

This project focuses on **backend system design**, not UI.

---

## 🏗 High-Level Architecture

```

Client
|
| HTTP (REST)
v
FastAPI API Layer
|
| SQLAlchemy ORM
v
Database (Jobs, Executions)
|
| BackgroundTasks
v
Execution Worker
|
| subprocess
v
Script Execution (Python / Bash)

```

**Key idea:**
Job execution is **decoupled** from request handling.

---

## 🧩 Tech Stack

- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **SQLite** — local development database
- **BackgroundTasks** — asynchronous execution
- **Pydantic** — request/response validation

---

## 📁 Project Structure

```

app/
├── main.py # Application entry point
├── database.py # DB engine & session
├── models.py # SQLAlchemy ORM models
├── schemas.py # Pydantic schemas
├── routers/
│ ├── jobs.py # Job CRUD APIs
│ └── executions.py # Execution APIs
├── services/
│ └── executor.py # Job execution logic
└── config.py # App configuration

```

---

## ⚙️ Setup & Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/PravarAgarwal/automation-ops-platform.git
cd automation-platform
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start the server

```bash
uvicorn app.main:app --reload
```

Server will be available at:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 📌 Example Usage

### Create a Job

```http
POST /jobs
```

```json
{
  "name": "hello-world",
  "script_type": "python",
  "script_content": "print('Hello from execution')"
}
```

---

### Run a Job

```http
POST /executions/{job_id}/run
```

Response:

```json
{
  "execution_id": 1,
  "status": "PENDING"
}
```

---

### Check Execution Status

```http
GET /executions/{execution_id}
```

```json
{
  "id": 1,
  "job_id": 1,
  "status": "SUCCESS",
  "stdout": "Hello from execution\n",
  "stderr": "",
  "exit_code": 0,
  "created_at": "...",
  "finished_at": "..."
}
```

---

## 🔐 Execution Safety

The system includes safeguards against:

- **Infinite loops** (execution timeout)
- **Long-running scripts**
- **Blocking API threads**

### Example test case

```python
while True:
    pass
```

Result:

- Execution fails gracefully
- API remains responsive

---

## 🔄 Why BackgroundTasks (Not Celery)?

This project intentionally starts with **FastAPI BackgroundTasks** to keep the system simple and understandable.

### Tradeoffs

| BackgroundTasks | Celery              |
| --------------- | ------------------- |
| Simple setup    | Distributed workers |
| Single-process  | Horizontal scaling  |
| Good for demos  | Production-grade    |

📌 **Future versions** can migrate execution to Celery + Redis.

---

## ✅ System Guarantees

- API requests are never blocked by job execution
- Infinite loops are safely terminated via execution timeout
- Output size is capped to prevent memory or database issues
- Concurrent execution of the same job is prevented
- Execution state is fully persisted and queryable
- System health can be checked via `/health`

## 🚧 Known Limitations

- BackgroundTasks are not suitable for distributed workloads
- SQLite is used for local development only
- No authentication/authorization yet
- Script execution is not sandboxed

These are **intentional design choices** for clarity.

---

## 🔮 Future Improvements

- Migrate execution to Celery + Redis
- Add per-job execution time limits
- Add retries & scheduling
- Add authentication
- Containerized execution (Docker)
- Frontend dashboard

---

## 🙌 Author

Built as a learning and portfolio project to demonstrate backend system design and asynchronous execution patterns.
