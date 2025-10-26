# 🧰 Mini-CRM "Repair Requests"

A simple repair request management system built with **FastAPI**, **SQLAlchemy (async)**, **Alembic**, **JWT Auth**, and containerized via **Docker**.

## 🚀 Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic (migrations)
- Pydantic v2
- Docker & Docker Compose
- GitHub Actions (CI/CD)

## ⚙️ Features
✅ JWT Authentication (admin / worker)  
✅ CRUD for users (admin only)  
✅ Create public repair requests (clients)  
✅ Assign workers to tickets  
✅ Ticket status update & filtering  
✅ Pagination on all list endpoints  
✅ Search by request title  
✅ Role-based permissions (admin vs worker)

## 🧩 Project Structure

```
app/
 ├── main.py               # FastAPI entry point
 ├── models/               # SQLAlchemy ORM models
 ├── routers/              # API routes
 ├── crud/                 # Database access logic
 ├── schemas/              # Pydantic models
 ├── core/                 # JWT, config, utils
 └── alembic/              # Migrations
```

## 🔑 Test Accounts

| Role   | Email               | Password  |
|--------|---------------------|------------|
| Admin  | admin@example.com   | admin123   |
| Worker | worker@example.com  | worker123  |


## 🐳 Local Run (from Docker Hub image)

1. Create file `.env` in root of project follow `.env.sample` structure.  
2. Run:
   ```bash
   docker-compose up -d
   ```
3. After running swagger will be able on url:
   ```
   http://localhost:8000/docs
   ```

Swagger docs: 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧰 Deliverables

- **GitHub Repository:** `https://github.com/endernaga/Mini-CRM-Repair-Requests.git`
- **Docker Hub Image:** `docker.io/endernaga/repairapp:latest`
- **Test Accounts:** admin / worker
- **Run instructions:** `docker-compose up -d`
