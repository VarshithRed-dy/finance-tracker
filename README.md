# Personal Finance Tracker API

A RESTful backend that lets users track their income and expenses. Each user registers, logs in to receive a JWT, and can then create, query, update, and delete their own transactions, view aggregated monthly analytics, and export their data as CSV. Every endpoint is scoped to the authenticated user, so no one can read or modify another person's data. Built with FastAPI and SQLAlchemy, it runs on SQLite locally and PostgreSQL in production.

**Live demo:** https://web-production-d7250.up.railway.app/docs
**Repository:** https://github.com/VarshithRed-dy/finance-tracker

> The live link opens FastAPI's interactive Swagger UI, where every endpoint can be tested in the browser.

---

## Tech Stack

| Technology | Why it's used |
|---|---|
| **FastAPI** | Modern async Python web framework. Generates interactive API docs automatically and validates requests from type hints. |
| **SQLAlchemy** | ORM that maps Python classes to database tables, so the same code runs against SQLite and PostgreSQL without changes. |
| **Pydantic** | Validates incoming/outgoing data and keeps the API layer separate from the database layer (passwords are never returned). |
| **PostgreSQL** | Production database — persistent and networked, survives container restarts. |
| **SQLite** | Local development database — zero setup, just a file on disk. |
| **JWT (python-jose)** | Stateless authentication. A signed token carries the user's identity, verified with a secret key. |
| **passlib + bcrypt** | One-way, salted, deliberately-slow password hashing. Plaintext passwords are never stored. |
| **python-dotenv** | Loads secrets (e.g. `SECRET_KEY`) from environment variables instead of hardcoding them. |
| **Uvicorn** | ASGI server that runs the app. |
| **Railway** | Hosting platform with a managed PostgreSQL instance. |

---

## API Endpoints

Auth required means the request must include a valid JWT (`Authorization: Bearer <token>`).

### General

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/` | Health check — confirms the API is running | No |

### Users

| Method | Path | Description | Auth |
|---|---|---|---|
| POST | `/users/register` | Create a new account (username, email, password) | No |
| POST | `/users/login` | Log in and receive a JWT access token | No |

### Transactions

| Method | Path | Description | Auth |
|---|---|---|---|
| POST | `/transactions/` | Create a transaction for the logged-in user | Yes |
| GET | `/transactions/` | List own transactions; supports filters (`type`, `category`, `start_date`, `end_date`) and pagination (`page`, `limit`) | Yes |
| GET | `/transactions/{id}` | Get a single transaction (only if it belongs to the user) | Yes |
| PATCH | `/transactions/{id}` | Partially update a transaction | Yes |
| DELETE | `/transactions/{id}` | Delete a transaction | Yes |
| GET | `/transactions/export/csv` | Download all own transactions as a CSV file | Yes |

### Analytics

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/analytics/summary` | Total income, expense, and net savings for a given `month` and `year` | Yes |
| GET | `/analytics/category-breakdown` | Totals grouped by category and type for a given `month` and `year` | Yes |
| GET | `/analytics/trends` | Monthly income/expense totals across all history, in chronological order | Yes |

---

## Running Locally

```bash
# 1. Clone and enter the project
git clone https://github.com/VarshithRed-dy/finance-tracker
cd finance-tracker

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file in the project root
#    Generate a secret with:  python -c "import secrets; print(secrets.token_hex(32))"
echo "SECRET_KEY=your-generated-secret-here" > .env

# 5. Run the server
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs**. With no `DATABASE_URL` set, the app automatically uses a local `finance.db` SQLite file.

### Authenticating in the docs

1. Register a user via `POST /users/register`.
2. Click the **Authorize** button (top right) and log in.
3. Protected endpoints are now unlocked.

---

## Project Structure

```
finance-tracker/
├── main.py            # App entry point, router wiring, global error handler
├── database.py        # SQLAlchemy engine/session; SQLite or PostgreSQL via DATABASE_URL
├── models.py          # SQLAlchemy models (User, Transaction)
├── schemas.py         # Pydantic request/response schemas + validation
├── auth.py            # Password hashing and JWT creation/verification
├── routers/
│   ├── users.py       # Registration and login
│   ├── transactions.py# CRUD, filtering, pagination, CSV export
│   └── analytics.py   # Aggregation endpoints
├── Procfile           # Start command for deployment
├── requirements.txt
└── README.md
```

---

## What I Learned

- **Separating database models from API schemas.** SQLAlchemy models define the tables; Pydantic schemas define what enters and leaves the API. Keeping them apart is what makes it impossible to accidentally return a password hash.
- **Stateless authentication with JWT.** A token's validity (signature + expiry) is verified using only the secret key — no database lookup needed to know whether a token is trustworthy.
- **Enforcing data ownership in the query, not the client.** Every transaction query is filtered by `user_id`, so one user physically cannot reach another's data, even by guessing IDs.
- **SQL aggregation through an ORM.** Using `GROUP BY` and `SUM` lets the database do the math and return just the answer, instead of pulling every row into Python.
- **Why SQLite breaks in production — firsthand.** After deploying, the app crashed because a SQLite-only connection setting (`check_same_thread`) was being passed to PostgreSQL. Tracing it through the deploy logs taught me that production needs a separate, persistent database and config that adapts to its environment.

## What I'd Add Next

- **Automated tests** with `pytest` covering auth, ownership rules, and the analytics math.
- **Database migrations** with Alembic, instead of creating tables on startup.
- **Refresh tokens** so sessions can outlive short-lived access tokens safely.
- **Exact money types** — switch `amount` from `Float` to `Numeric`/`Decimal` to avoid floating-point rounding on financial sums.
- **Richer pagination** — return total counts and page metadata in list responses.
- **Rate limiting** on the login and register endpoints to slow down brute-force attempts.