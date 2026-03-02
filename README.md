# Django REST API — Dockerized

A scalable **Django REST Framework** backend with PostgreSQL, JWT auth, versioned API routing, and OpenAPI docs. Fully containerized with Docker.

---

## Project Structure

```bash
├── apps                # All Django applications
│   └── accounts
│   └── ..              
├── engine/             # Core settings, urls, wsgi, asgi
│   └── settings.py
│   └── ..  
├── endpoints/          # Versioned API routing (v1/, v2/, ...)
│   └── v1
│   └── ..  
├── kernel/             # Shared base classes and utilities
├── docs/               # OpenAPI 3.0 specification files
│   └── openapi.yml
│   └── ..  
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── request.http
├── pytest.ini
├── README.md
└── .env
```

---

## Features

- JWT Authentication via **SimpleJWT**
- Role-based access control with custom permission classes
- Full **CRUD APIs** across all modules
- Versioned API routing (`/api/v1/`, `/api/v2/`)
- **PostgreSQL** as the primary database
- Fully **Dockerized** development and production environment
- Interactive **OpenAPI / Swagger** documentation

---

## Requirements

- Docker & Docker Compose v2+
- Python 3.12 *(runs inside container — no local install required)*
- PostgreSQL 15+ *(provided via Docker)*

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/anmamuncoder/your-project.git
cd your-project
```

**2. Create `.env` file in the project root**
```dotenv
COMPOSE_PROJECT_NAME=your_project_name
WEB_PORT=8020
DB_PORT=5433

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_NAME=your_db_name
POSTGRES_USER=django
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

TIME_ZONE=Asia/Dhaka
LANGUAGE_CODE=en-us
```

**3. Build and run**
```bash
sudo docker compose up --build -d
sudo docker compose exec web python manage.py migrate
sudo docker compose exec web python manage.py createsuperuser
```

---

## Docker Commands

| Command | Description |
|---|---|
| `sudo docker compose up --build -d` | Build and start containers |
| `sudo docker compose ps` | List running containers |
| `sudo docker compose exec web bash` | Shell into web container |
| `sudo docker compose logs -f` | Stream live logs |
| `sudo docker compose down` | Stop and remove containers |
| `sudo docker compose down -v` | Stop and wipe all data |

---

## Access Points

| Service     | URL                           |
|-------------|-------------------------------|
| API Root    | http://127.0.0.1:8020/api/v1/ |
| Admin Panel | http://127.0.0.1:8020/admin/  |
| Swagger UI  | http://127.0.0.1:8020/docs/   |
| Redoc       | http://127.0.0.1:8020/redoc/  |

---

## API Documentation

The `docs/` folder contains **OpenAPI 3.0** specification files:
```
docs/
└── openapi.yml     # Complete API schema — endpoints, request & response shapes
```

Compatible with:

- **Swagger UI** — interactive, browser-based API explorer
- **Redoc** — clean, human-readable API reference
- **Postman** — import the YAML to auto-generate a full request collection
  
---

## Development Tips

- Always run `migrate` after pulling changes that include new migrations
- Extend `kernel/` base classes to avoid repeating logic across apps
- Register all new apps under `apps/` and wire their routes in `endpoints/v1/`
- Use versioned endpoints from the start to maintain backward compatibility
- `POSTGRES_HOST=db` in `.env` refers to the Docker service name — do not change it for local development

---

## License

MIT License © 2026
*Built by* [anmamuncoder](https://anmamuncoder.vercel.app/) — *Software Engineer*