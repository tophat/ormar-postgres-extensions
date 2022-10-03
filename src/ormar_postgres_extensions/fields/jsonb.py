from typing import Any

import ormar
from sqlalchemy.dialects import postgresql


def jsonb_contained_by(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column <@ VALUE::jsonb`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="jsonb_contained_by", other=other)


def jsonb_contains(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column @> VALUE::jsonb`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="jsonb_contains", other=other)


# Need to patch the filter objects to support JSONB specifc actions
FIELD_ACCESSOR_MAP = [
    ("jsonb_contained_by", jsonb_contained_by),
    ("jsonb_contains", jsonb_contains),
]


for (method_name, method) in FIELD_ACCESSOR_MAP:
    setattr(ormar.queryset.FieldAccessor, method_name, method)


# These lines allow Ormar to lookup the new filter methods and map
# it to the correct PGSQL functions
ACCESSOR_MAP = [
    ("jsonb_contained_by", "contained_by"),
    ("jsonb_contains", "contains"),
]

for (ormar_operation, pg_operation) in ACCESSOR_MAP:
    ormar.queryset.actions.filter_action.FILTER_OPERATORS[
        ormar_operation
    ] = pg_operation
    ormar.queryset.actions.filter_action.METHODS_TO_OPERATORS[
        ormar_operation
    ] = ormar_operation


class JSONB(ormar.JSON):
    """
    Custom JSON field uses a native PG JSONB type
    """

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.JSONB:
        return postgresql.JSONB()
