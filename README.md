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

---

## Desarrollo Local

### Usando Docker Compose (Recomendado)

```bash
# Iniciar aplicación con MySQL
docker-compose up --build

# La aplicación corre en http://localhost:8080
```

### Usando Solo Docker

```bash
# Construir imagen
docker build -t bluelabel-app .

# Ejecutar contenedor
docker run -p 8080:8080 --env-file .env bluelabel-app
```

### Usando Python

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
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

| Secret | Descripción |
|:-------|:------------|
| `GCP_PROJECT_ID` | ID del proyecto en Google Cloud |
| `GCP_SA_KEY` | JSON key de la Service Account |
| `DEV_DB_HOST` | Host de la BD de DEV |
| `DEV_DB_USER` | Usuario de la BD de DEV |
| `DEV_DB_PASSWORD` | Contraseña de la BD de DEV |
| `PROD_DB_HOST` | Host de la BD de PROD |
| `PROD_DB_USER` | Usuario de la BD de PROD |
| `PROD_DB_PASSWORD` | Contraseña de la BD de PROD |
| `VPC_CONNECTOR` | Nombre del Serverless VPC Connector |
| `GCP_SERVICE_ACCOUNT` | Email de la Service Account de runtime |

> Algunos secrets listados están pensados para la arquitectura objetivo de producción y se documentan por completitud.

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
