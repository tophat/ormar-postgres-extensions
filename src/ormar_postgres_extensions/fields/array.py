from typing import (
    Any,
    Optional,
)

import ormar
from sqlalchemy.dialects import postgresql


def array_contains(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column @> ARRAY[<VALUE>]`

    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="array_contains", other=other)


def array_contained_by(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column <@ ARRAY[<VALUE>]`

    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="array_contained_by", other=other)


def array_overlap(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column && ARRAY[<VALUE>]`

    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="array_overlap", other=other)


# Need to patch the filter objects to support array specifc actions
FIELD_ACCESSOR_MAP = [
    ("array_contains", array_contains),
    ("array_contained_by", array_contained_by),
    ("array_overlap", array_overlap),
]


for (method_name, method) in FIELD_ACCESSOR_MAP:
    setattr(ormar.queryset.FieldAccessor, method_name, method)


# These lines allow Ormar to lookup the new filter methods and map
# it to the correct PGSQL functions
ACCESSOR_MAP = [
    ("array_contains", "contains"),
    ("array_contained_by", "contained_by"),
    ("array_overlap", "overlap"),
]

for (ormar_operation, pg_operation) in ACCESSOR_MAP:
    ormar.queryset.actions.filter_action.FILTER_OPERATORS[
        ormar_operation
    ] = pg_operation
    ormar.queryset.actions.filter_action.METHODS_TO_OPERATORS[
        ormar_operation
    ] = ormar_operation


class ARRAY(ormar.fields.model_fields.ModelFieldFactory, list):
    _type = list
    _sample = []

    def __new__(  # type: ignore
        cls, *, item_type, dimensions: Optional[int] = None, **kwargs: Any
    ) -> ormar.fields.BaseField:
        return super().__new__(
            cls, **{**kwargs, "item_type": item_type, "dimensions": dimensions}
        )

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.ARRAY:
        return postgresql.ARRAY(kwargs["item_type"], dimensions=kwargs["dimensions"])
