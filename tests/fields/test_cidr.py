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


class CidrTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    cidr: IPAddress = ormar_pg_ext.CIDR()


class NullableCidrTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    cidr: Optional[IPAddress] = ormar_pg_ext.CIDR(nullable=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip, ip_type",
    [
        # IP V4
        ("192.168.0.1/32", IPv4Interface),
        # IP V6
        ("::ffff:c0a8:1/128", IPv6Interface),
    ],
)
async def test_create_model_with_cidr_address_specified(db, ip, ip_type):
    created = await CidrTestModel(cidr=ip_interface(ip)).save()
    assert str(created.cidr) == ip
    assert isinstance(created.cidr, ip_type)

    # Confirm the model got saved to the DB by querying it back
    found = await CidrTestModel.objects.get()
    assert found.cidr == created.cidr
    assert isinstance(found.cidr, ip_type)


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
async def test_create_model_with_cidr_network_specified(db, ip, ip_type):
    created = await CidrTestModel(cidr=ip_interface(ip)).save()
    assert str(created.cidr) == ip
    assert isinstance(created.cidr, ip_type)

    # Confirm the model got saved to the DB by querying it back
    found = await CidrTestModel.objects.get()
    assert found.cidr == created.cidr
    assert isinstance(found.cidr, ip_type)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip",
    [
        "192.168.0.1",
        "::ffff:c0a8:1",
    ],
)
async def test_get_model_by_cidr(db, ip):
    created = await CidrTestModel(cidr=ip_address(ip)).save()

    found = await CidrTestModel.objects.filter(cidr=ip_address(ip)).all()
    assert len(found) == 1
    assert found[0] == created


@pytest.mark.asyncio
async def test_create_model_with_nullable_cidr(db):
    created = await NullableCidrTestModel().save()
    assert created.cidr is None


@pytest.mark.asyncio
async def test_get_model_with_nullable_cidr(db):
    created = await NullableCidrTestModel().save()

    # Ensure querying a model with a null UUID works
    found = await NullableCidrTestModel.objects.get()
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
async def test_cidr_contained_by(db, ip, contained, expected):
    created = await CidrTestModel(cidr=ip).save()

    found = await CidrTestModel.objects.filter(cidr__contained_by=contained).all()

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
async def test_cidr_contained_by_eq(db, ip, contained, expected):
    created = await CidrTestModel(cidr=ip).save()

    found = await CidrTestModel.objects.filter(cidr__contained_by_eq=contained).all()

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
    created = await CidrTestModel(cidr=ip).save()

    found = await CidrTestModel.objects.filter(cidr__contains_subnet=contained).all()

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
async def test_cidr_contains_subnet_eq(db, ip, contained, expected):
    created = await CidrTestModel(cidr=ip).save()

    found = await CidrTestModel.objects.filter(cidr__contains_subnet_eq=contained).all()

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
async def test_cidr_contains_or_eq(db, ip, contained, expected):
    created = await CidrTestModel(cidr=ip).save()

    found = await CidrTestModel.objects.filter(cidr__contains_or_eq=contained).all()

    if expected:
        assert len(found) == 1
        assert found[0] == created
    else:
        assert len(found) == 0
