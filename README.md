# Supabase Auth API

A production-minded authentication API built with FastAPI and Supabase Auth. Supabase owns password hashing, sessions, JWT signing, and user verification; this API provides a documented backend boundary around those capabilities.

## Features

- Email/password signup, login, and logout
- Reusable Bearer-token dependency for protected routes
- Swagger UI with an `Authorize` button at `/docs`
- ReDoc at `/redoc`
- Strict environment-based configuration
- Offline tests for the route contract and auth guard

## Structure

```text
app/
├── main.py                 # FastAPI application and middleware
├── config.py               # Settings and Supabase client factory
├── dependencies.py         # Reusable Supabase token guard
├── schemas.py              # Pydantic request and response models
└── routers/
    ├── auth.py             # Signup, login, logout
    └── profile.py          # Public and protected examples
tests/
└── test_api.py             # Offline API contract tests
```

## Setup

Requirements: Python 3.10+ and a Supabase project.

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
```

Set the values in `.env`:

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_anon_key
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

Use the public `anon` key. Never use the Supabase `service_role` key in this API.

In Supabase, configure Authentication -> Sign In / Providers -> Email. During local development, you may disable email confirmation; production applications should keep verification enabled.

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs).

## Endpoints

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/` | Public health check |
| POST | `/auth/signup` | Public |
| POST | `/auth/login` | Public |
| POST | `/auth/logout` | Bearer token |
| GET | `/public/info` | Public |
| GET | `/protected/profile` | Bearer token |
| GET | `/protected/dashboard` | Bearer token |

After login, click **Authorize** in Swagger UI and paste the returned `access_token` without the `Bearer` prefix.

## Test

```bash
pytest
```

Logout ends the Supabase client session. Because access tokens are stateless JWTs, an already-issued token can remain valid until its expiry; use short token lifetimes or a server-side revocation strategy if immediate invalidation is required.
