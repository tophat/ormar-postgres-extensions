from typing import Any

import ormar
from sqlalchemy.dialects import postgresql


class MACADDR(ormar.fields.model_fields.ModelFieldFactory, str):
    _type = str

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.MACADDR:
        # Tell Ormar that this column should be a postgres macaddr type
        return postgresql.MACADDR()
