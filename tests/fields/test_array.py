from typing import Optional

import ormar
import pytest
from sqlalchemy import String
from sqlalchemy.dialects import postgresql

from ormar_postgres_extensions.fields import Array
from tests.database import (
    database,
    metadata,
)


class ArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: list = Array(item_type=String())


class NullableArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: Optional[list] = Array(item_type=String(), nullable=True)


@pytest.mark.asyncio
async def test_create_model_with_array(db):
    created = await ArrayTestModel(data=["a", "b"]).save()
    assert created.data == ["a", "b"]

    # Confirm the model got saved to the DB by querying it back
    found = await ArrayTestModel.objects.get()
    assert found.data == ["a", "b"]


@pytest.mark.asyncio
async def test_create_model_with_nullable_array(db):
    created = await NullableArrayTestModel().save()
    assert created.data is None

    found = await NullableArrayTestModel.objects.get()
    assert found.data is None


@pytest.mark.asyncio
async def test_filter_array_column(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c"]).save()

    print(ArrayTestModel.data)

    found = await ArrayTestModel.objects.filter(
        (ArrayTestModel.data.contains(["c"]))
    ).get()

    assert len(found) == 1
