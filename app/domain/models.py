"""
Domain models.

This module defines domain-level data structures used across the application.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class User:
    """Represent a registered user.

    Store the user's unique `id` and `email` address.
    """

    id: UUID
    email: str