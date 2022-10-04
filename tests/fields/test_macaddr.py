from typing import Optional

import ormar
import pytest

import ormar_postgres_extensions as ormar_pg_ext
from tests.database import (
    database,
    metadata,
)


class MacAddrTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    addr: str = ormar_pg_ext.MACADDR()


class NullableMacAddrTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    addr: Optional[str] = ormar_pg_ext.MACADDR(nullable=True)


@pytest.mark.asyncio
async def test_create_model_with_macaddr_specified(db):
    created = await MacAddrTestModel(addr="08:00:2b:01:02:03").save()
    assert str(created.addr) == "08:00:2b:01:02:03"
    assert isinstance(created.addr, str)

    # Confirm the model got saved to the DB by querying it back
    found = await MacAddrTestModel.objects.get()
    assert found.addr == created.addr
    assert isinstance(found.addr, str)


@pytest.mark.asyncio
async def test_get_model_by_macaddr(db):
    created = await MacAddrTestModel(addr="08:00:2b:01:02:03").save()

    found = await MacAddrTestModel.objects.filter(addr="08:00:2b:01:02:03").all()
    assert len(found) == 1
    assert found[0] == created


@pytest.mark.asyncio
async def test_create_model_with_nullable_macaddr(db):
    created = await NullableMacAddrTestModel().save()
    assert created.addr is None


@pytest.mark.asyncio
async def test_get_model_with_nullable_macaddr(db):
    created = await NullableMacAddrTestModel().save()

    # Ensure querying a model with a null UUID works
    found = await NullableMacAddrTestModel.objects.get()
    assert found == created
