# 🚀 BlueLab DevOps Test

Aplicación Flask de prueba con conexión a MySQL, containerizada con Docker.

## 📋 Requisitos

- Python 3.11+
- Docker
- MySQL 8.0+

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
# Editar .env con tus credenciales

# Ejecutar la aplicación
python -m app.main
```

## 🐳 Docker

```bash
# Construir imagen
docker build -t bluelabel-devops-test:latest .

# Ejecutar contenedor
docker run -p 8080:8080 --env-file .env bluelabel-devops-test:latest
```

## 🔗 Endpoints

| Método | Ruta | Descripción |
|:-------|:-----|:------------|
| GET | `/health` | Health check, retorna estado y entorno |
| GET | `/info` | Obtiene mensaje desde la base de datos |

## 📁 Estructura del Proyecto

```
├── app/
│   ├── __init__.py
│   ├── config.py      # Configuración de variables de entorno
│   ├── db.py          # Conexión a MySQL
│   └── main.py        # Endpoints Flask
├── .env.example       # Template de variables de entorno
├── Dockerfile         # Multi-stage build con usuario no-root
├── requirements.txt   # Dependencias Python (versiones pinneadas)
└── .gitignore
```

## 🔐 Variables de Entorno

| Variable | Descripción | Default |
|:---------|:------------|:--------|
| `APP_ENV` | Entorno de ejecución | `dev` |
| `DB_HOST` | Host de MySQL | - |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_NAME` | Nombre de la base de datos | - |
| `DB_USER` | Usuario de MySQL | - |
| `DB_PASSWORD` | Contraseña de MySQL | - |

## 📄 Licencia

MIT
