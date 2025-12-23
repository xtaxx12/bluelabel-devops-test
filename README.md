# BlueLabel DevOps - Prueba Técnica

Aplicación backend en Flask que demuestra mejores prácticas de DevOps y Cloud: containerización, configuración basada en entorno, pipelines CI/CD y arquitectura lista para producción.

---

## Requisitos

- Python 3.11+
- Docker & Docker Compose
- MySQL 8.0+

---

## Decisiones Técnicas

- Se eligió Flask por su simplicidad y claridad.
- Se usó Docker para garantizar consistencia entre entornos.
- Se seleccionó GitHub Actions para CI/CD por su integración nativa con GitHub.
- Se prefirió Cloud Run sobre GKE para reducir la carga operativa.

## Próximos Pasos (Producción)

- Habilitar facturación de GCP y provisionar Cloud SQL con IP privada
- Configurar Serverless VPC Connector
- Agregar monitoreo con Cloud Monitoring y alertas
- Implementar migraciones de base de datos

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                     Repositorio GitHub                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                          │
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
│   Cloud SQL (Privado)    │    │   Cloud SQL (Privado)    │
│   DB: app_dev            │    │   DB: app_prod           │
└──────────────────────────┘    └──────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                ▼
                ┌──────────────────────────┐
                │     Red Privada VPC      │
                │  Serverless VPC Connector│
                └──────────────────────────┘
```
> ⚠️ El siguiente diagrama representa la **arquitectura objetivo de producción**.  
> El entorno de evaluación utiliza una base de datos containerizada debido a restricciones de facturación en GCP.

---

## Desarrollo Local

### Usando Docker Compose (Recomendado)

```bash

docker-compose up --build


```

### Usando Solo Docker

```bash

docker build -t bluelabel-app .


docker run -p 8080:8080 --env-file .env bluelabel-app
```

### Usando Python

```bash

python -m venv .venv


.venv\Scripts\activate


source .venv/bin/activate


pip install -r requirements.txt

python -m app.main
```

---

## Endpoints de la API

| Método | Ruta | Descripción |
|:-------|:-----|:------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/info` | Mensaje de la base de datos |

### Ejemplos

**Endpoint Raíz**
```bash
curl http://localhost:8080/
```
Respuesta:
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
Respuesta:
```json
{
  "status": "ok",
  "env": "dev"
}
```

**Info de Base de Datos**
```bash
curl http://localhost:8080/info
```
Respuesta:
```json
{
  "message": "Hello from DEV"
}
```

---

## Variables de Entorno

| Variable | Descripción | Default |
|:---------|:------------|:--------|
| `APP_ENV` | Entorno (dev/prod) | `dev` |
| `DB_HOST` | Host de MySQL | - |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_NAME` | Nombre de la base de datos | - |
| `DB_USER` | Usuario de MySQL | - |
| `DB_PASSWORD` | Contraseña de MySQL | - |

---

## Pipeline CI/CD

### Visión General del Pipeline

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
                   │   (Automático)     │                         │(Aprobación Manual) │
                   └────────────────────┘                         └────────────────────┘
```

> Nota: El diagrama anterior representa la **arquitectura objetivo de producción**.  
> Debido a restricciones de facturación de GCP, el entorno de evaluación usa una configuración de base de datos simplificada, detallada más abajo.

### Workflows

| Workflow | Trigger | Descripción |
|:---------|:--------|:------------|
| `ci.yml` | Push/PR a main | Lint, test, validación de build |
| `deploy-dev.yml` | Push a main | Deploy automático a DEV |
| `deploy-prod.yml` | Tag v* o push a prod | Deploy a PROD con gate de aprobación |

### Deploy a DEV
- **Trigger:** Push a rama `main`
- **Proceso:** Automático
- **Pasos:** Test → Build → Deploy

### Deploy a PROD
- **Trigger:** Tag `v*` (ej: v1.0.0) o push a rama `prod`
- **Proceso:** Requiere aprobación manual
- **Pasos:** Test → Build → Gate de Aprobación → Deploy

### Secrets de GitHub Requeridos

| Secret | Descripción | Requerido |
|--------|-------------|-----------|
| `GCP_PROJECT_ID` | ID del proyecto en GCP | ✅ |
| `GCP_SA_KEY` | JSON de la Service Account | ✅ |

---

## Guía de Deploy a GCP

### Paso 1: Configurar Proyecto en GCP

```bash
# Crear proyecto (o usar uno existente)
gcloud projects create PROJECT_ID --name="BlueLabel App"

# Establecer proyecto activo
gcloud config set project PROJECT_ID

# Habilitar APIs necesarias
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

### Paso 2: Crear Artifact Registry

```bash
gcloud artifacts repositories create bluelabel-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="BlueLabel Docker images"
```

### Paso 3: Crear Service Account

```bash
# Crear Service Account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

# Asignar roles necesarios
PROJECT_ID=$(gcloud config get-value project)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Generar key JSON
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@${PROJECT_ID}.iam.gserviceaccount.com
```

### Paso 4: Configurar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Agregar los siguientes secrets:

| Secret | Valor |
|--------|-------|
| `GCP_PROJECT_ID` | Tu Project ID de GCP |
| `GCP_SA_KEY` | Contenido completo del archivo `key.json` |

### Paso 5: Configurar Environments en GitHub

1. Settings → Environments
2. Crear environment `development`
3. Crear environment `production` con:
   - ✅ Required reviewers (agregar aprobadores)
   - ✅ Wait timer (opcional)

### Paso 6: Desplegar

**DEV (automático):**
```bash
git push origin main
```

**PROD (con aprobación):**
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Verificar Deploy

```bash
# Ver servicios desplegados
gcloud run services list --region=us-central1

# Ver logs
gcloud run services logs read bluelabel-app-dev --region=us-central1
```

### Eliminar Recursos (Cleanup)

```bash
# Eliminar servicios de Cloud Run
gcloud run services delete bluelabel-app-dev --region=us-central1 --quiet
gcloud run services delete bluelabel-app-prod --region=us-central1 --quiet

# Eliminar repositorio de Artifact Registry
gcloud artifacts repositories delete bluelabel-repo --location=us-central1 --quiet
```

---

## Estructura del Proyecto

```
├── .github/
│   └── workflows/
│       ├── ci.yml              # Pipeline CI
│       ├── deploy-dev.yml      # Deploy a DEV
│       └── deploy-prod.yml     # Deploy a PROD
├── app/
│   ├── __init__.py
│   ├── config.py               # Configuración de entorno
│   ├── db.py                   # Conexión a base de datos
│   └── main.py                 # Endpoints Flask
├── tests/
│   ├── conftest.py             # Fixtures de Pytest
│   └── test_endpoints.py       # Tests unitarios
├── docs/                       # Carpeta para capturas de pantalla
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml          # Desarrollo local
├── Dockerfile                  # Build multi-stage
├── init.sql                    # Inicialización de BD
└── requirements.txt
```

---

## URLs en la Nube

| Entorno | URL |
|:--------|:----|
| DEV | No desplegado (entorno de evaluación) |
| PROD | No desplegado (entorno de evaluación) |

---

## Arquitectura de Base de Datos

### Configuración de Producción
- Cloud SQL MySQL con IP privada
- Conectividad por red VPC
- Serverless VPC Connector para Cloud Run

### Entorno de Evaluación
Debido a requisitos de facturación de GCP, no se provisionó Cloud SQL. Se usa MySQL containerizado local para demostración.

| Componente | Evaluación | Producción |
|:-----------|:-----------|:-----------|
| Base de datos | MySQL en Docker | Cloud SQL |
| Red | Red de Docker | IP privada VPC |
| Conexión | Directa | VPC Connector |

---

## Seguridad

- Sin credenciales en el repositorio
- Variables de entorno para datos sensibles
- Imagen Docker base mínima (python:slim)
- Usuario no-root en el contenedor
- Acceso basado en IAM con privilegios mínimos

---

## Ejecutar Tests

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov

# Ejecutar tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ -v --cov=app
```

---

## Licencia

MIT
