import uuid
from typing import (
    Any,
    Optional,
)

import ormar
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.types import TypeDecorator


class PostgresUUIDTypeDecorator(TypeDecorator):
    """
    Postgres specific GUID type for user with Ormar
    """

    impl = postgresql.UUID

    def process_literal_param(
        self, value: Optional[uuid.UUID], dialect: DefaultDialect
    ) -> Optional[str]:
        # Literal parameters for PG UUID values need to be quoted inside
        # of single quotes
        return f"'{value}'" if value is not None else None

    def process_bind_param(
        self, value: Optional[uuid.UUID], dialect: DefaultDialect
    ) -> Optional[str]:
        return str(value) if value is not None else None

    def process_result_value(
        self, value: Optional[str], dialect: DefaultDialect
    ) -> Optional[uuid.UUID]:
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


class UUID(ormar.UUID):
    """
    Custom UUID field for the schema that uses a native PG UUID type
    """

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> PostgresUUIDTypeDecorator:
        # Tell Ormar that this column should be a postgres UUID type
        return PostgresUUIDTypeDecorator()
