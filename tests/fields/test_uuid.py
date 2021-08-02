from typing import Optional
from uuid import (
    UUID,
    uuid4,
)

import ormar
import pytest

from ormar_postgres_extensions.fields import PostgresUUID
from tests.database import (
    database,
    metadata,
)


class UUIDTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    uid: UUID = PostgresUUID(default=uuid4)


class NullableUUIDTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    uid: Optional[UUID] = PostgresUUID(nullable=True)


@pytest.mark.asyncio
async def test_create_model_with_uuid_specified(db):
    created = await UUIDTestModel(uid="2b077a49-0dbe-4dd1-88a1-9aebe3cb7653").save()
    assert str(created.uid) == "2b077a49-0dbe-4dd1-88a1-9aebe3cb7653"
    assert isinstance(created.uid, UUID)

    # Confirm the model got saved to the DB by querying it back
    found = await UUIDTestModel.objects.get()
    assert found.uid == created.uid
    assert isinstance(found.uid, UUID)


@pytest.mark.asyncio
async def test_get_model_by_uuid(db):
    created = await UUIDTestModel(uid="2b077a49-0dbe-4dd1-88a1-9aebe3cb7653").save()

    found = await UUIDTestModel.objects.filter(
        uid="2b077a49-0dbe-4dd1-88a1-9aebe3cb7653"
    ).all()
    assert len(found) == 1
    assert found[0] == created


@pytest.mark.asyncio
async def test_create_model_with_nullable_uuid(db):
    created = await NullableUUIDTestModel().save()
    assert created.uid is None


@pytest.mark.asyncio
async def test_get_model_with_nullable_uuid(db):
    created = await NullableUUIDTestModel().save()

    # Ensure querying a model with a null UUID works
    found = await NullableUUIDTestModel.objects.get()
    assert found == created
