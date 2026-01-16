# Contributing to BE-User-System

Thanks for contributing! This project follows lightweight contribution rules to keep changes focused and reviewable.

Checklist
- Create a small, focused branch: `feature/your-topic` or `fix/issue-description`.
- Run tests locally and ensure they pass: `py -m pytest -q`.
- Add tests for bug fixes or new features.
- Keep changes and commits small and atomic.

Local setup
1. Copy the example env file and set secrets locally:

```powershell
copy .env.example .env
```

2. Create and activate a Python virtual environment and install deps:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Testing and style
- Run the test suite: `py -m pytest -q`.
- (Optional) Run static checks such as `mypy` if present in CI.

Pull Request guidelines
- Open a PR against `main` with a descriptive title and short summary.
- Reference any related issue and include before/after notes if relevant.
- Keep PRs small to simplify review.

Thanks — maintainers will review and request changes if needed.
