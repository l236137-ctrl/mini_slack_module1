# Mini Slack Backend

A simplified Slack clone backend, built incrementally as an intern learning project.

## Tech Stack

Python 3.13 · Django 5.x · Django REST Framework · PostgreSQL 16 · JWT auth (`djangorestframework-simplejwt`)

## Global API conventions

- Base path: `/api/v1/`
- JSON only (`Content-Type: application/json`)
- Auth: `Authorization: Bearer <access_token>` on everything except `/register`, `/login`, and `/health`
- Success: `{"success": true, "data": {...}}`
- Error: `{"success": false, "error": {"code": "...", "message": "...", "fields": {...}}}`
- Pagination: `?page=1&page_size=20` (max 100) → `{"count", "next", "previous", "results"}`
- Timestamps: ISO 8601 UTC
- IDs: UUID everywhere (including the custom `User` model, so this had to be decided in Module 1 — Django won't let you swap the user model after the first migration)

These are implemented once, project-wide, in the `core` app:

| File | Responsibility |
|---|---|
| `core/renderers.py` | `EnvelopeJSONRenderer` — wraps every response in `{success, data}` / relies on the exception handler for the error shape |
| `core/exceptions.py` | `envelope_exception_handler` — converts any DRF exception into the standard error envelope |
| `core/pagination.py` | `StandardPageNumberPagination` — `page`/`page_size`, max 100 |
| `core/models.py` | `BaseModel` — abstract base giving every future model a UUID pk + `created_at`/`updated_at` |

Every new module should build on top of these rather than reinventing them.

## Project layout

```
mini_slack/
├── manage.py
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── mini_slack/            # project package
│   ├── settings/
│   │   ├── base.py         # shared config
│   │   ├── dev.py          # DEBUG=True, console logging
│   │   └── prod.py         # security hardening, no wildcard hosts
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py             # ready for Channels in Module 12+
├── core/                  # shared utilities (envelope, pagination, base model)
└── accounts/              # custom User model (UUID pk)
```

## Setup

### Option A — Docker (recommended)

```bash
cp .env.example .env          # edit values as needed
docker compose up --build
```

The API will be available at `http://localhost:8000/api/v1/`. Migrations don't run automatically — run them once the containers are up:

```bash
docker compose exec web python manage.py migrate
```

### Option B — Local virtualenv

Requires a local PostgreSQL 16 server already running.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # edit SECRET_KEY, DATABASE_URL, etc.

python manage.py migrate
python manage.py createsuperuser # optional, for /admin
python manage.py runserver
```

By default `manage.py` and `wsgi.py` point at `mini_slack.settings.dev`. For production, set `DJANGO_SETTINGS_MODULE=mini_slack.settings.prod` (and make sure `ALLOWED_HOSTS`, `SECRET_KEY`, `DATABASE_URL` are set in the real environment — `prod.py` has no unsafe defaults).

### Running tests

```bash
python manage.py test
```

## Endpoints (Module 1)

| Method | Path | Auth required | Description |
|---|---|---|---|
| `GET` | `/api/v1/health` | No | Returns `{"status": "ok", "db": "connected"}` (200) if the DB is reachable, or `{"status": "error", "db": "disconnected"}` (503) if not. **Not** wrapped in the standard envelope and **not** JWT-protected — infra health checks (load balancers, k8s probes) expect a plain, unauthenticated, fixed-shape response here. |

Future modules will document their endpoints in this same table as they land.

## Notes / decisions worth knowing about

- **Custom `User` model from day one.** Even though registration/login endpoints are a later module, `AUTH_USER_MODEL` had to be pointed at `accounts.User` before the first migration, since Django makes changing it afterwards extremely painful. The model currently just adds a UUID primary key and a unique, required email — auth-flow-specific fields will be added in Module 2.
- **`requirements.txt` versions.** Pinned to a specific, known-compatible set (Django 5.1.4, DRF 3.15.2, etc.). After your first real `pip install`, run `pip freeze > requirements.txt` to lock in whatever your environment actually resolved, per the Definition of Done.
- **Health check bypasses the global envelope/auth conventions on purpose** (see table above) — this is the one deliberate exception to the global rules, called out explicitly so it doesn't look like a bug in review.
