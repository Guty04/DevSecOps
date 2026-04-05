# DevSecOps Backend

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
## Arquitectura

```text
📂 migrations/             # Migraciones de base de datos (Alembic)
📂 src/
 ├── 📂 configurations/    # Gestión de configuración
 ├── 📂 constants/         # Constantes globales del sistema
 ├── 📂 database/          # Modelos de SQLAlchemy y conexión
 ├── 📂 enums/             # Enumeraciones y tipos definidos
 ├── 📂 errors/            # Manejo centralizado de excepciones
 ├── 📂 locales/           # Archivos de traducción
 ├── 📂 repositories/      # Capa de acceso a datos
 ├── 📂 routes/            # Routers y dependencias
 ├── 📂 schemas/           # Esquemas de validación
 ├── 📂 services/          # Lógica de negocio y casos de uso
 ├── 📂 utils/             # Utilidades y helpers
 └── main.py
📂 tests/
 ├── 📂 e2e/               # Pruebas end-to-end
 ├── 📂 integration/       # Pruebas de integración
 └── 📂 unit/              # Pruebas unitarias
```

## Comenzando

### Prerrequisitos

- **Docker** y **Docker Compose**
- **Python 3.13+**
- **uv** (recomendado para gestión de paquetes)

### Instalación Local

```bash
# Clonar el repositorio
git clone <repository-url>
cd devsecops

# Crear entorno virtual e instalar dependencias
uv sync

# Activar el entorno
source .venv/bin/activate

# Instalar pre-commit hooks
pre-commit install
```

### Ejecución con Docker

```bash
# Iniciar servicios (Base de Datos + API)
docker-compose up --build

# Acceder a la documentación interactiva
# Scalar: http://localhost:8000/docs
# Swagger: http://localhost:8000/openapi.json
```

## Desarrollo y Seguridad

El proyecto utiliza diversas herramientas para garantizar la calidad y seguridad del código:

- **Linter/Formatter:** [Ruff](https://github.com/astral-sh/ruff) para mantener un código limpio y consistente.
- **Seguridad:** [Bandit](https://github.com/PyCQA/bandit) para análisis estático de vulnerabilidades.
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/) para el control de versiones de la base de datos.
- **i18n:** Soporte multilingüe (Español/Inglés) usando **Babel**.

## Comandos Útiles

```bash
# Ejecutar tests
pytest

# Aplicar migraciones
alembic upgrade head

# Formatear código
ruff format .
```
