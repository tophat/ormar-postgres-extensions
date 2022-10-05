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


class PostgresCidrTypeDecorator(TypeDecorator):
    """
    Postgres specific CIDR type for user with Ormar

    A custom TypeDecorator is needed here to be able to access the operators
    that are not provided by SQLAlchemy directly as functions. These are implemented
    inside of the comparator_factory class
    """

    impl = postgresql.CIDR

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


class CIDR(ormar.fields.model_fields.ModelFieldFactory, str):
    _type = Union[IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> postgresql.CIDR:
        return PostgresCidrTypeDecorator()
