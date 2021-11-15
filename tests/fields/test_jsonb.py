import json
from typing import Optional

import ormar
import pytest

from ormar_postgres_extensions.fields import JSONB
from tests.database import (
    database,
    metadata,
)


class JSONBTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: dict = JSONB()


class NullableJSONBTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: Optional[dict] = JSONB(nullable=True)


@pytest.mark.asyncio
async def test_create_model_with_jsonb(db):
    created = await JSONBTestModel(data=json.dumps(dict(foo="bar"))).save()
    assert created.data == {"foo": "bar"}

    # Confirm the model got saved to the DB by querying it back
    found = await JSONBTestModel.objects.get()
    assert found.data == {"foo": "bar"}


@pytest.mark.asyncio
async def test_create_model_with_nullable_jsonb(db):
    created = await NullableJSONBTestModel().save()
    assert created.data is None

    found = await NullableJSONBTestModel.objects.get()
    assert found.data is None
