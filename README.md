# BE: Clean Architecture — User Registration API

A small, well-tested User Registration API demonstrating Clean Architecture principles, separation of concerns, and easy testability.

Key goals:

- Keep business rules independent from frameworks and infrastructure.
- Make persistence replaceable (memory / SQLite) without changing domain code.
- Provide a clear, testable HTTP adapter (FastAPI) and decoupled authentication.

## Problem

Implement a maintainable, testable User Registration API where users can register with an email address. The system should emphasize:

- Centralized business rules
- Swap-able persistence
- Documented HTTP surface
- Authentication decoupled from domain logic
- Layered testing (unit, integration, API)

## Architecture Overview

The project follows Clean Architecture: the domain layer has no framework dependencies; infrastructure and adapters can be replaced independently.

```txt
         ┌─────────────┐
         │   FastAPI   │  ← HTTP / JWT
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │ Application │  ← Dependency Injection
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │   Domain    │  ← Business Rules
         └──────┬──────┘
                │
      ┌─────────▼─────────┐
      │ Repositories      │
      │ (Memory / SQLite) │
      └───────────────────┘
```

## Design Decisions

- Pure domain: the domain layer does not depend on FastAPI, SQLite, or JWT.
- Changeable infrastructure: repository implementations (in-memory and SQLite) follow the same contract.
- Decoupled authentication: JWT is handled in the HTTP layer; the domain is unaware of auth details.
- External validation: Pydantic validates DTOs in the HTTP layer; domain receives already-validated data.
- Dependency injection: simple manual DI in the application layer with test-friendly overrides.

## Testing Strategy

- Unit tests: domain logic covered thoroughly.
- Integration tests: verify repository and application wiring.
- API tests: ensure HTTP endpoints behave as expected.

All tests assert behavior rather than internal implementation details.

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

3. Run tests:

```bash
py -m pytest
```

## Future Work

- Add a simple frontend for registration
- Support additional authentication methods
- Expand integration and end-to-end test coverage
- Containerize with Docker and add CI/CD

## License

This project is licensed under the GNU General Public License v3.0 — see the [LICENSE](LICENSE) file for details.
