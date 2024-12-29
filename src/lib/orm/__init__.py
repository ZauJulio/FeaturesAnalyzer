"""ORM: Object Relational Mapping with strict types."""


class FAORMError(Exception):
    """Custom error class for FAORM operations."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


from . import db

__all__ = ["FAORMError", "db"]
