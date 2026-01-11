# BE: Clean Architecture - User Registration API

This project is a simple backend User Registration API built using the **Clean Architecture** principles, **responsability separation** and **testability** in mind.

The project objective is to demonstrate architecture desingn concepts:

- Pure Domain Layer
- Changeable Infrastructure Layer
- External Adapters (HTTP, Database, CLI)

## Problem Statement

Register users securely and consistently, ensuring:

- Centralized bussiness logic
- Persistence changeability
- documented HTTP API
- Decoupled authentication
- Multiple-layer testing

## Architecture Overview

The system follows the Clean Architecture principles:

- The domain doesn't depend on any frameworks.
- The infrastructure layer can be swapped without affecting the domain.
- The adapters translate, they don't make decisions.

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

## Technical Desicions

### Pure Domain Layer

- It doesn't depend on FastAPI, SQLite or JWT
- 100% test coverage with unit tests

### Changeable Infrastructure Layer

- Repositories implemented with in-memory and SQLite
- Same contracts, it won't affect the domain

### Decoupled Authentication

- JWT handled in FastAPI layer
- Domain unaware of authentication mechanism

### External Validation

- DTO validation with Pydantic in FastAPI layer
- Domain receives already validated data

### Dependency Injection

- Simple manual DI in FastAPI layer
- Clean overrides for testing

## Testing Strategy

- Unit Tests for Domain Layer (100% coverage)
- Integration Tests for Application Layer
- Tests for dependency container
- API tests for HTTP endpoints

All tests validate behavior, not implementation details.

## How to Run

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

## Conclusion

In this project, I have learned and applied Clean Architecture principles to build a User Registration API that is maintainable, testable, and adaptable to change. The separation of concerns allows for easy modifications and enhancements in the future. Some difficulties were faced in ensuring complete decoupling between layers, but these were overcome through careful design, rethinking, and iterative testing. Overall, this project serves as a solid foundation for me to build more complex systems and leave room for future improvements.

Feel free to explore the codebase and reach out if you have any questions or suggestions!

## Future Improvements

- Add frontend interface
- Implement more authentication methods
- Expand test coverage to integration tests
- Containerize the application with Docker
- Implement CI/CD pipeline for automated testing and deployment

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
