<!--
BE-User-System
Clean Architecture — User Registration API

This README follows common software-project documentation practices:
- clear title and description
- table of contents for quick navigation
- reproducible quickstart and development steps
- architecture and design rationale
-->

# BE: Clean Architecture — User Registration API

Small, well-tested User Registration API demonstrating Clean Architecture
principles: keep business rules independent from frameworks, make
persistence swappable, and keep the HTTP adapter thin and testable.

## Table of contents

- [Quickstart](#quickstart)
- [Development](#development)
- [Architecture](#architecture)
- [Design decisions](#design-decisions)
- [Testing strategy](#testing-strategy)
- [Project layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)

## Quickstart

Run the project locally for development in three steps.

1. Create and activate a virtual environment (Windows example):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

3. Start the API (development server):

```powershell
# Preferred: run the module that contains the FastAPI app
uvicorn app.api.http:app --reload

# Alternative: the project re-exports the app at app.main
uvicorn app.main:app --reload
```

### Configuration

This project uses an explicit `Settings` dataclass (`app.core.config.Settings`) as
the single source of configuration. Applications should call `load_settings()` and
pass the returned `Settings` instance into the `Container`:

```python
from app.core.config import load_settings
from app.core.container import Container

settings = load_settings()
container = Container(settings)
```

Key environment variables:
- `APP_ENV` — environment name (defaults to `development`)
- `SECRET_KEY` — secret signing key for JWT tokens (recommended to set in production)
- `DB_PATH` — path to the SQLite database file (defaults to `app/schemas/users.db`)

A `.env.example` file is provided at the repository root. Copy it to `.env` and adjust values during local development:

```powershell
copy .env.example .env
```

For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

4. Run tests:

```powershell
py -m pytest -q
```

## Development

- Use the virtual environment to avoid global package conflicts.
- Keep tests fast: prefer unit tests for domain logic and run them
  frequently during development.
- Use the `Container` to obtain repository and service instances in
  integration tests.

## Architecture

The project follows Clean Architecture / Hexagonal principles. Layers and responsibilities:

- HTTP adapter: FastAPI endpoints, DTOs and authentication (`app/api`).
- Application wiring: minimal `Container` that provides repository and service factories (`app/core`).
- Domain: business rules and models (`app/domain`).
- Repositories: storage backends (in-memory and SQLite) implementing the repository contract (`app/repos`).

ASCII overview:

```txt
         ┌─────────────┐
         │   FastAPI   │  ← HTTP adapter, DTOs, auth
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │ Application │  ← Container / wiring
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │   Domain    │  ← services, models, business rules
         └──────┬──────┘
                │
      ┌─────────▼─────────┐
      │    Repositories   │  ← storage backends (SQLite / memory)
      └───────────────────┘
```

## Design decisions

- Domain-first: domain code has no FastAPI/DB/JWT dependencies.
- Explicit, test-friendly DI: `Container` returns new instances on demand.
- Thin HTTP layer: fastAPI handles validation and auth, but delegates
  business rules to domain services.
- Repositories are swappable: implementations follow the `UserRepository`
  interface so storage can be changed without touching domain logic.

## Testing strategy

- Unit tests: test `UserService` and domain behavior in isolation.
- Integration tests: test repository implementations and wiring.
- API tests: exercise HTTP endpoints using FastAPI's TestClient.

Run all tests:

```powershell
py -m pytest -q
```

Notes for Windows: temporary files used in SQLite tests may be briefly locked
by the runtime; tests include a small retry loop on cleanup to reduce flakiness.

## Project layout

Top-level folders:

- `app/` — application source (API adapters, core, domain, repos)
- `tests/` — unit, integration and API tests

Quick references:

- Application entry: [app/main.py](app/main.py)
- FastAPI app: [app/api/http.py](app/api/http.py)
- Domain: [app/domain/models.py](app/domain/models.py), [app/domain/services.py](app/domain/services.py)
- SQLite repo: [app/repos/sqlite.py](app/repos/sqlite.py)

## Contributing

- Open small, focused pull requests.
- Add tests for new behavior or bug fixes.
- Follow the project's docstring and typing conventions.

## License

This project is licensed under the GNU General Public License v3.0 — see the [LICENSE](LICENSE) file for details.

---
