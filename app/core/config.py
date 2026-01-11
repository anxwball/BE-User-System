import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    env: str
    debug: bool

def load_settings() -> Settings:
    env = os.getenv("APP_ENV", "development")
    debug = env != "production"
    return Settings(env=env, debug=debug)