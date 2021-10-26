from typing import Any

import ormar
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator


class PostgresArrayTypeDecorator(TypeDecorator):
    impl = postgresql.ARRAY

    def __init__(self, item_type, *args, **kwargs):
        super().__init__(item_type, *args, **kwargs)
        self._item_type = item_type

    def load_dialect_impl(self, dialect: Dialect):
        return postgresql.ARRAY(self._item_type)


class Array(ormar.fields.model_fields.ModelFieldFactory, list):
    _type = list
    _sample = []

    def __new__(  # type: ignore
        cls, *, item_type, **kwargs: Any
    ) -> ormar.fields.BaseField:
        return super().__new__(cls, **{**kwargs, "item_type": item_type})

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> PostgresArrayTypeDecorator:
        return PostgresArrayTypeDecorator(item_type=kwargs["item_type"])
