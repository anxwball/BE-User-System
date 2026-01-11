import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

@dataclass(frozen=True)
class Settings:
    env: str
    debug: bool
    secret_key: Optional[str] = None

def load_settings() -> Settings:
    env = os.getenv("APP_ENV", "development")
    debug = env != "production"
    secret_key = os.getenv("SECRET_KEY")
    return Settings(env=env, debug=debug, secret_key=secret_key)


def get_module_secret(module_name: str) -> str:
    candidates = [
        f"{module_name.upper()}_SECRET_KEY",
        f"{module_name.upper()}_SEC_KEY",
        "SECRET_KEY",
    ]
    for name in candidates:
        val = os.getenv(name)
        if val:
            return val
    raise RuntimeError(
        f"No secret key found for module '{module_name}'. Set one of: {', '.join(candidates)}"
    )