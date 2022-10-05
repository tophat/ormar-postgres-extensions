from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv6Address,
    IPv6Interface,
    ip_address,
    ip_interface,
)
from typing import (
    Optional,
    Union,
)

import ormar
import pytest

import ormar_postgres_extensions as ormar_pg_ext
from tests.database import (
    database,
    metadata,
)

IPAddress = Union[
    IPv4Address,
    IPv4Interface,
    IPv6Address,
    IPv6Interface,
]


class InetTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    inet: IPAddress = ormar_pg_ext.INET()


class NullableInetTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    inet: Optional[IPAddress] = ormar_pg_ext.INET(nullable=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, ip_type",
    [
        # IP V4
        ("192.168.0.1", IPv4Address),
        # IP V6
        ("::ffff:c0a8:1", IPv6Address),
    ],
)
async def test_create_model_with_inet_address_specified(db, ip, ip_type):
    created = await InetTestModel(inet=ip_address(ip)).save()
    assert str(created.inet) == ip
    assert isinstance(created.inet, ip_type)

    # Confirm the model got saved to the DB by querying it back
    found = await InetTestModel.objects.get()
    assert found.inet == created.inet
    assert isinstance(found.inet, ip_type)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, ip_type",
    [
        # IP V4 Subnet
        ("192.168.1.0/24", IPv4Interface),
        # IP V6 Subnet
        ("2001:db8::/120", IPv6Interface),
    ],
)
async def test_create_model_with_inet_network_specified(db, ip, ip_type):
    created = await InetTestModel(inet=ip_interface(ip)).save()
    assert str(created.inet) == ip
    assert isinstance(created.inet, ip_type)

    # Confirm the model got saved to the DB by querying it back
    found = await InetTestModel.objects.get()
    assert found.inet == created.inet
    assert isinstance(found.inet, ip_type)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip",
    [
        "192.168.0.1",
        "::ffff:c0a8:1",
    ],
)
async def test_get_model_by_inet(db, ip):
    created = await InetTestModel(inet=ip_address(ip)).save()

    found = await InetTestModel.objects.filter(inet=ip_address(ip)).all()
    assert len(found) == 1
    assert found[0] == created


@pytest.mark.asyncio
async def test_create_model_with_nullable_inet(db):
    created = await NullableInetTestModel().save()
    assert created.inet is None


@pytest.mark.asyncio
async def test_get_model_with_nullable_inet(db):
    created = await NullableInetTestModel().save()

    # Ensure querying a model with a null UUID works
    found = await NullableInetTestModel.objects.get()
    assert found == created


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, contained, expected",
    [
        (ip_address("192.168.1.5"), ip_interface("192.168.1.0/24"), True),
        (ip_address("192.168.0.5"), ip_interface("192.168.1.0/24"), False),
        (ip_interface("192.168.1.0/24"), ip_interface("192.168.1.0/24"), False),
    ],
)
async def test_inet_contained_by(db, ip, contained, expected):
    created = await InetTestModel(inet=ip).save()

    found = await InetTestModel.objects.filter(inet__contained_by=contained).all()

    if expected:
        assert len(found) == 1
        assert found[0] == created
    else:
        assert len(found) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, contained, expected",
    [
        (ip_address("192.168.1.5"), ip_interface("192.168.1.0/24"), True),
        (ip_address("192.168.0.5"), ip_interface("192.168.1.0/24"), False),
        (ip_interface("192.168.1.0/24"), ip_interface("192.168.1.0/24"), True),
    ],
)
async def test_inet_contained_by_eq(db, ip, contained, expected):
    created = await InetTestModel(inet=ip).save()

    found = await InetTestModel.objects.filter(inet__contained_by_eq=contained).all()

    if expected:
        assert len(found) == 1
        assert found[0] == created
    else:
        assert len(found) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, contained, expected",
    [
        (ip_interface("192.168.1.0/24"), ip_address("192.168.1.5"), True),
        (ip_interface("192.168.1.0/24"), ip_address("192.168.2.5"), False),
        (ip_interface("192.168.1.0/24"), ip_interface("192.168.1.0/24"), False),
    ],
)
async def test_contains_subnet(db, ip, contained, expected):
    created = await InetTestModel(inet=ip).save()

    found = await InetTestModel.objects.filter(inet__contains_subnet=contained).all()

    if expected:
        assert len(found) == 1
        assert found[0] == created
    else:
        assert len(found) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, contained, expected",
    [
        (ip_interface("192.168.1.0/24"), ip_address("192.168.1.5"), True),
        (ip_interface("192.168.1.0/24"), ip_address("192.168.2.5"), False),
        (ip_interface("192.168.1.0/24"), ip_interface("192.168.1.0/24"), True),
    ],
)
async def test_inet_contains_subnet_eq(db, ip, contained, expected):
    created = await InetTestModel(inet=ip).save()

    found = await InetTestModel.objects.filter(inet__contains_subnet_eq=contained).all()

    if expected:
        assert len(found) == 1
        assert found[0] == created
    else:
        assert len(found) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, contained, expected",
    [
        (ip_interface("192.168.1.0/24"), ip_interface("192.168.1.80/28"), True),
        (ip_interface("192.168.1.0/24"), ip_interface("192.168.2.0/28"), False),
    ],
)
async def test_inet_contains_or_eq(db, ip, contained, expected):
    created = await InetTestModel(inet=ip).save()

    found = await InetTestModel.objects.filter(inet__contains_or_eq=contained).all()

    if expected:
        assert len(found) == 1
        assert found[0] == created
    else:
        assert len(found) == 0
