# GeoPort Logistics Backend API

A lightweight, high-performance, and production-structured REST API engine for a logistics and cargo tracking application. Built using Python 3.12, FastAPI, SQLAlchemy ORM, and Pydantic validation, with JWT authentication guards and Redis-backed service states.

---

## 🏗️ Architecture Design Principles

The backend features a clean, highly scalable domain-layered architecture. Dependencies flow inward toward core security functions and schema-bound databases, guaranteeing separation of concerns and simpler testing patterns.

```
backend/
├── app/
│   ├── api/             # HTTP Route Handlers / Endpoints
│   ├── core/            # Cryptography, JWT, App Config Settings
│   ├── database/        # Database Connection Configuration
│   ├── models/          # SQLAlchemy Database Schemas
│   ├── schemas/         # Pydantic Structural Serialization Schemas
│   ├── services/        # Business Logic Actions
│   ├── repositories/    # Database Layer Abstraction
│   ├── utils/           # Resilient Helpers (e.g. Caching with Local Fallback)
│   └── main.py          # Entrypoint & Automatic Boot Metadata Seeding
├── tests/               # Isolation Pytest Suites (using memory SQL)
├── requirements.txt     # Global Application Dependencies
└── .env.example         # System Environment Variable Templates
```

### 💎 Key Engineering Highlight: Resilient Caching Fallback
To provide maximal ecosystem compatibility, the `CacheService` utilizes a **local fallback mechanism**. If the application cannot connect to a running Redis server:
1. It registers a warning log.
2. It immediately shifts caching operations to a thread-safe local dictionary cache with expiration tracking.
This guarantees startup stability across local workstations, testing targets, and standard CI environments.

---

## 🛠️ Technology Stack
* **Python 3.12+**
* **FastAPI**: Core async REST framework
* **SQLAlchemy 2.0+**: Structural SQL ORM maps
* **Pydantic v2**: High-speed, typings-bound JSON parsing & validations
* **SQLite / PostgreSQL-ready**: Automatic structural conversions
* **Redis-py**: High-speed query response cache
* **Passlib (Bcrypt)**: Secure password cryptographic hashing
* **Python-jose**: Signed JSON Web Tokens (JWT)
* **Pytest**: Automated integration testing suite

---

## 🚦 Environment Constants (`.env`)

Configure these values in your workspace `.env` file (copied from `.env.example`):

| Variable | Default Value | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///./logistics.db` | Target SQL connection locator |
| `SECRET_KEY` | *(A random 64-char string)* | Cryptographic seed for signing JWTs |
| `ALGORITHM` | `HS256` | Target signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Duration before token authentication expires |
| `REDIS_HOST` | `localhost` | Redis caching daemon address |
| `REDIS_PORT` | `6379` | Redis caching port |

---

## 🚀 Execution Instructions

### 1. Local Setup
Ensure Python 3.12+ is installed, then initialize a python virtual environment and download packages:

```bash
# Clone the repository and navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate
# Activate on Windows
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Copy Environment Templates
```bash
cp .env.example .env
```

### 3. Boot Redis
Ensure you have Redis running in the background. Or simply skip, and the application will gracefully run using the internal mock in-memory cache!
```bash
# Start redis-server inside Docker or locally
docker run -d --name geoport-redis -p 6379:6379 redis:alpine
```

### 4. Running the FastAPI Server
Run the live uvicorn process. Since database creation is dynamic, tables are automatically bootstrapped and default items are seeded onto standard files.
```bash
uvicorn app.main:app --reload --port 3000
```

---

## 🛡️ Live Seeding Sandbox Credentials
On first start, the system seeds some default information to help test and review functionalities:
* **Administrator Profile**:
  * **Email**: `admin@geoportlogistics.com`
  * **Password**: `admin123`
* **Pre-manufactured Shipment tracking number**: `GP123456`
* **Logistics category services**: Road freight, Sea cargo, and Storage-depot categories.

---

## 🧪 Running Automated Pytest Suites

Pytest operates in a isolated testing workspace using rapid in-memory SQLite fixtures. To trigger testing scripts run:

```bash
pytest
```

---

## 📑 Interactive Documentation

Your live sandbox features interactive documentation interfaces natively under:
* **Swagger UI / OpenAPI Interactive Specification**: [http://localhost:3000/docs](http://localhost:3000/docs)
* **ReDoc Design Schema**: [http://localhost:3000/redoc](http://localhost:3000/redoc)
