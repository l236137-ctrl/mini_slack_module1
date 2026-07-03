## 1. Project Overview

**Title:** Mini Slack Backend
**Purpose:** An incremental intern project that teaches authentication, relational data modeling, REST API design, permissions, and real-time communication by building a simplified Slack clone backend.

**Tech Stack**

| Layer | Choice |
|---|---|
| Language | Python 3.13+ |
| Framework | Django 5.x |
| API Layer | Django REST Framework (DRF) |
| Database | PostgreSQL 16+ |
| Real-time | Django Channels + Redis (Module 12+) |
| Auth | JWT (via `djangorestframework-simplejwt`) |
| Containerization | Docker + docker-compose (optional but recommended) |
| Version Control | Git/GitHub with PR-based workflow |

**Definition of Done (applies to every module):**
- All listed endpoints implemented and manually tested via Postman/curl
- Input validation on every field with meaningful 400 error messages
- Permission checks enforced (not just documented)
- Unit tests covering happy path + at least 2 failure cases per endpoint
- Migrations committed
- README updated with new endpoints

---

## 2. Global API Conventions

These rules apply to **every** module, not just one — stating them once here instead of repeating per-module.

- **Base path:** all endpoints are prefixed with `/api/v1/`
- **Format:** JSON request/response bodies only, `Content-Type: application/json`
- **Auth header:** `Authorization: Bearer <access_token>` on all endpoints except `/register` and `/login`
- **Standard success envelope:**
  ```json
  { "success": true, "data": { ... } }
  ```
- **Standard error envelope:**
  ```json
  { "success": false, "error": { "code": "VALIDATION_ERROR", "message": "...", "fields": {"field_name": "reason"} } }
  ```
- **Pagination** (any list endpoint): query params `?page=1&page_size=20` (max page_size = 100), response includes `count`, `next`, `previous`, `results`
- **Timestamps:** ISO 8601 UTC (`created_at`, `updated_at`)
- **IDs:** UUID (not auto-increment integers) — avoids leaking record counts and workspace/channel enumeration
- **HTTP status codes to use consistently:**
  - `200` OK, `201` Created, `204` No Content (deletes)
  - `400` validation error, `401` not authenticated, `403` authenticated but not authorized, `404` not found, `409` conflict (e.g., duplicate username), `429` rate-limited

---

## 3. Module 1 — Project Setup

### Goal
Bootstrap the project with a working, version-controlled connection to PostgreSQL.

### Requirements
1. Django project named `mini_slack`, first app `accounts`
2. `.env` file (git-ignored) holding `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `ALLOWED_HOSTS`
3. `.env.example` committed with placeholder values
4. `requirements.txt` pinned to exact versions (`pip freeze`)
5. Settings split into `settings/base.py`, `settings/dev.py`, `settings/prod.py`
6. Health check endpoint: `GET /api/v1/health` → `200 {"status": "ok", "db": "connected"}`

### Acceptance Criteria
- `python manage.py migrate` runs cleanly against Postgres
- `/api/v1/health` returns 200 with DB connectivity confirmed (not hardcoded)
- Secrets are never committed to Git

---
