# 🚀 BlueLabel DevOps - Prueba Técnica

Aplicación backend basada en Flask, diseñada para demostrar mejores prácticas en DevOps y Cloud, incluyendo containerización, configuración basada en entorno y arquitectura lista para producción.

---

## 📋 Requisitos

- Python 3.11+
- Docker
- MySQL 8.0+

---

## 🏃 Ejecución Local

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar la aplicación
python -m app.main
```

---

## 🐳 Docker

```bash
# Construir imagen
docker build -t bluelabel-app .

# Ejecutar contenedor
docker run -p 8080:8080 --env-file .env bluelabel-app
```

---

## 🔗 Endpoints

| Método | Ruta | Descripción |
|:-------|:-----|:------------|
| GET | `/health` | Health check, retorna estado y entorno |
| GET | `/info` | Obtiene mensaje desde la base de datos |

---

## 📁 Estructura del Proyecto

```
├── app/
│   ├── __init__.py
│   ├── config.py      # Configuración de variables de entorno
│   ├── db.py          # Conexión a MySQL
│   └── main.py        # Endpoints Flask
├── .env.example       # Plantilla de variables de entorno
├── Dockerfile         # Multi-stage build con usuario no-root
├── requirements.txt   # Dependencias Python (versiones pinneadas)
└── .gitignore
```

---

## 🔐 Variables de Entorno

| Variable | Descripción | Default |
|:---------|:------------|:--------|
| `APP_ENV` | Entorno de ejecución | `dev` |
| `DB_HOST` | Host de MySQL | - |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_NAME` | Nombre de la base de datos | - |
| `DB_USER` | Usuario de MySQL | - |
| `DB_PASSWORD` | Contraseña de MySQL | - |

---

## 🧱 Visión General de la Arquitectura

La aplicación sigue una arquitectura simple y limpia:

- ✅ Aplicación Flask ejecutándose en un contenedor Docker
- ✅ Configuración gestionada mediante variables de entorno
- ✅ Diseño stateless, adecuado para plataformas de orquestación de contenedores
- ✅ Base de datos accedida a través de una capa de conexión configurable

---

## 🌍 Estrategia de Despliegue (Cloud)

### Plataforma Objetivo

**Google Cloud Run**

### Entornos

| Entorno | Tipo de Despliegue |
|:--------|:-------------------|
| **DEV** | Despliegues automáticos |
| **PROD** | Despliegues controlados con aprobación manual |

> Cada entorno utiliza sus propios valores de configuración y base de datos.

---

## 🔄 Estrategia CI/CD (Planificada)

El pipeline de CI/CD está diseñado de la siguiente manera:

### DEV
- **Trigger:** push a `main`
- **Pasos:** build → test → dockerize → deploy a Cloud Run (DEV)

### PROD
- **Trigger:** merge a `prod`
- **Pasos:** build → puerta de aprobación → deploy a Cloud Run (PROD)

---

## 🔐 Consideraciones de Seguridad

- ✅ **Sin credenciales en el repositorio** - Los secretos nunca se almacenan en código
- ✅ **Variables de entorno** - Los valores sensibles se inyectan en tiempo de ejecución
- ✅ **Imagen Docker mínima** - Se usa imagen base `slim` para reducir superficie de ataque
- ✅ **Usuario no-root** - El contenedor corre sin privilegios de root
- ✅ **IAM y least-privilege** - En producción se aplicarían políticas de acceso mínimo

---

## 🗄️ Arquitectura de Base de Datos (Producción vs Evaluación)

Debido a los requisitos de facturación de Google Cloud, Cloud SQL no pudo ser provisionado en este entorno de evaluación.

| Escenario | Solución |
|:----------|:---------|
| **Evaluación** | Instancia MySQL containerizada local |
| **Producción** | Cloud SQL con IP privada, VPC y Serverless VPC Connector |

> Este enfoque garantiza transparencia mientras se mantienen los principios de diseño de grado producción.

---

## 📄 Licencia

MIT
