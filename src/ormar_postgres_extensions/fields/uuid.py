from typing import Any

import ormar
from sqlalchemy.dialects import postgresql


class UUID(ormar.UUID):
    """
    Custom UUID field for the schema that uses a native PG UUID type
    """

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.UUID:
        # Tell Ormar that this column should be a postgres UUID type
        return postgresql.UUID()
