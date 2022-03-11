from typing import Any

import ormar
from sqlalchemy.dialects import postgresql


class JSONB(ormar.JSON):
    """
    Custom JSON field uses a native PG JSONB type
    """

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.JSONB:
        return postgresql.JSONB()
