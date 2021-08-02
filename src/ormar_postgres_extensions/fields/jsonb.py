from typing import Any

import ormar
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import TypeDecorator


class PostgresJSONBTypeDecorator(TypeDecorator):
    impl = postgresql.JSONB


class PostgresJSONB(ormar.JSON):
    """
    Custom JSON field uses a native PG JSONB type
    """

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> PostgresJSONBTypeDecorator:
        return PostgresJSONBTypeDecorator()
