# BlueLabel DevOps - Technical Test

Flask backend application demonstrating DevOps and Cloud best practices: containerization, environment-based configuration, CI/CD pipelines, and production-ready architecture.

---

## Requirements

- Python 3.11+
- Docker & Docker Compose
- MySQL 8.0+

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Actions CI/CD                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   Lint   │───▶│   Test   │───▶│  Build   │───▶│  Deploy  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│     Cloud Run (DEV)      │    │     Cloud Run (PROD)     │
│   bluelabel-app-dev      │    │   bluelabel-app-prod     │
│   APP_ENV=dev            │    │   APP_ENV=prod           │
└──────────────────────────┘    └──────────────────────────┘
                │                               │
                ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   Cloud SQL (Private)    │    │   Cloud SQL (Private)    │
│   DB: app_dev            │    │   DB: app_prod           │
└──────────────────────────┘    └──────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                ▼
                ┌──────────────────────────┐
                │    VPC Private Network   │
                │  Serverless VPC Connector│
                └──────────────────────────┘
```

---

## Local Development

### Using Docker Compose (Recommended)

```bash
# Start application with MySQL
docker-compose up --build

# Application runs at http://localhost:8080
```

### Using Docker Only

```bash
# Build image
docker build -t bluelabel-app .

# Run container
docker run -p 8080:8080 --env-file .env bluelabel-app
```

### Using Python

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m app.main
```

---

## API Endpoints

| Method | Route | Description |
|:-------|:------|:------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/info` | Database message |

### Examples

**Root Endpoint**
```bash
curl http://localhost:8080/
```
Response:
```json
{
  "service": "BlueLabel DevOps API",
  "version": "1.0.0",
  "status": "running",
  "env": "dev",
  "endpoints": ["/health", "/info"]
}
```

**Health Check**
```bash
curl http://localhost:8080/health
```
Response:
```json
{
  "status": "ok",
  "env": "dev"
}
```

**Database Info**
```bash
curl http://localhost:8080/info
```
Response:
```json
{
  "message": "Hello from BlueLabel DevOps!"
}
```

---

## Environment Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `APP_ENV` | Environment (dev/prod) | `dev` |
| `DB_HOST` | MySQL host | - |
| `DB_PORT` | MySQL port | `3306` |
| `DB_NAME` | Database name | - |
| `DB_USER` | MySQL user | - |
| `DB_PASSWORD` | MySQL password | - |

---

## CI/CD Pipeline

### Pipeline Overview

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│     LINT       │────▶│     TEST       │────▶│     BUILD      │
│  flake8/black  │     │    pytest      │     │    docker      │
└────────────────┘     └────────────────┘     └────────────────┘
                                                      │
                              ┌───────────────────────┴────────────────────────┐
                              ▼                                                ▼
                   ┌────────────────────┐                         ┌────────────────────┐
                   │    DEPLOY DEV      │                         │   DEPLOY PROD      │
                   │    (Automatic)     │                         │ (Manual Approval)  │
                   └────────────────────┘                         └────────────────────┘
```

### Workflows

| Workflow | Trigger | Description |
|:---------|:--------|:------------|
| `ci.yml` | Push/PR to main | Lint, test, build validation |
| `deploy-dev.yml` | Push to main | Automatic deploy to DEV |
| `deploy-prod.yml` | Tag v* or push to prod | Deploy to PROD with approval gate |

### DEV Deployment
- **Trigger:** Push to `main` branch
- **Process:** Automatic
- **Steps:** Test → Build → Deploy

### PROD Deployment
- **Trigger:** Tag `v*` (e.g., v1.0.0) or push to `prod` branch
- **Process:** Requires manual approval
- **Steps:** Test → Build → Approval Gate → Deploy

### GitHub Secrets Required

| Secret | Description |
|:-------|:------------|
| `GCP_PROJECT_ID` | Google Cloud project ID |
| `GCP_SA_KEY` | Service account JSON key |
| `DEV_DB_HOST` | DEV database host |
| `DEV_DB_USER` | DEV database user |
| `DEV_DB_PASSWORD` | DEV database password |
| `PROD_DB_HOST` | PROD database host |
| `PROD_DB_USER` | PROD database user |
| `PROD_DB_PASSWORD` | PROD database password |
| `VPC_CONNECTOR` | Serverless VPC connector name |
| `GCP_SERVICE_ACCOUNT` | Runtime service account email |

---

## Project Structure

```
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline
│       ├── deploy-dev.yml      # DEV deployment
│       └── deploy-prod.yml     # PROD deployment
├── app/
│   ├── __init__.py
│   ├── config.py               # Environment configuration
│   ├── db.py                   # Database connection
│   └── main.py                 # Flask endpoints
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   └── test_endpoints.py       # Unit tests
├── docs/                       # Screenshots folder
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml          # Local development
├── Dockerfile                  # Multi-stage build
├── init.sql                    # Database initialization
└── requirements.txt
```

---

## Cloud URLs

| Environment | URL | Status |
|:------------|:----|:-------|
| DEV | `https://bluelabel-app-dev-xxxxx.run.app` | Pending |
| PROD | `https://bluelabel-app-prod-xxxxx.run.app` | Pending |

---

## Database Architecture

### Production Setup
- Cloud SQL MySQL with private IP
- VPC network connectivity
- Serverless VPC Connector for Cloud Run

### Evaluation Environment
Due to GCP billing requirements, Cloud SQL was not provisioned. Local containerized MySQL is used for demonstration.

| Component | Evaluation | Production |
|:----------|:-----------|:-----------|
| Database | Docker MySQL | Cloud SQL |
| Network | Docker network | VPC private IP |
| Connection | Direct | VPC Connector |

---

## Security

- No credentials in repository
- Environment variables for sensitive data
- Minimal base Docker image (python:slim)
- Non-root container user
- IAM-based access with least privilege

---

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app
```

---

## License

MIT
