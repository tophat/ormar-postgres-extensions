from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv6Address,
    IPv6Interface,
)
from typing import (
    Any,
    Union,
)

import ormar
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import Operators
from sqlalchemy.types import TypeDecorator


def contained_by(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column << inet VALUE`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="contained_by", other=other)


def contained_by_eq(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column <<= inet VALUE`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="contained_by_eq", other=other)


def contains_subnet(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column >> inet VALUE`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="contains", other=other)


def contains_subnet_eq(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column >>= inet VALUE`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="contains_subnet_eq", other=other)


def contains_or_eq(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    works as postgresql `column >>= inet VALUE`
    :param other: value to check against operator
    :type other: Any
    :return: FilterGroup for operator
    :rtype: ormar.queryset.clause.FilterGroup
    """
    return self._select_operator(op="contains_or_eq", other=other)


# Need to patch the filter objects to support JSONB specifc actions
FIELD_ACCESSOR_MAP = [
    ("contained_by", contained_by),
    ("contained_by_eq", contained_by_eq),
    ("contains_subnet", contains_subnet),
    ("contains_subnet_eq", contains_subnet_eq),
    ("contains_or_eq", contains_or_eq),
]


for (method_name, method) in FIELD_ACCESSOR_MAP:
    setattr(ormar.queryset.FieldAccessor, method_name, method)


# These lines allow Ormar to lookup the new filter methods and map
# it to the correct PGSQL functions
ACCESSOR_MAP = [
    ("contained_by", "contained_by"),
    ("contained_by_eq", "contained_by_eq"),
    ("contains_subnet", "contains_subnet"),
    ("contains_subnet_eq", "contains_subnet_eq"),
    ("contains_or_eq", "contains_or_eq"),
]

for (ormar_operation, pg_operation) in ACCESSOR_MAP:
    ormar.queryset.actions.filter_action.FILTER_OPERATORS[
        ormar_operation
    ] = pg_operation
    ormar.queryset.actions.filter_action.METHODS_TO_OPERATORS[
        ormar_operation
    ] = ormar_operation


class PostgresInetTypeDecorator(TypeDecorator):
    """
    Postgres specific INET type for user with Ormar

    A custom TypeDecorator is needed here to be able to access the operators
    that are not provided by SQLAlchemy directly as functions. These are implemented
    inside of the comparator_factory class
    """

    impl = postgresql.INET

    class comparator_factory(postgresql.INET.Comparator):
        def contained_by(self, value):
            return Operators.op(self, "<<")(value)

        def contained_by_eq(self, value):
            return Operators.op(self, "<<=")(value)

        def contains_subnet(self, value):
            return Operators.op(self, ">>")(value)

        def contains_subnet_eq(self, value):
            return Operators.op(self, ">>=")(value)

        def contains_or_eq(self, value):
            return Operators.op(self, "&&")(value)


class INET(ormar.fields.model_fields.ModelFieldFactory, str):
    _type = Union[IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.INET:
        return PostgresInetTypeDecorator()
