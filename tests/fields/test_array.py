from typing import Optional

import ormar
import pytest
from sqlalchemy import (
    Integer,
    String,
)

from ormar_postgres_extensions.fields import ARRAY
from tests.database import (
    database,
    metadata,
)


class ArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: list = ARRAY(item_type=String())


class MultiDimensionArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: list = ARRAY(item_type=Integer(), dimensions=2)


class NullableArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: Optional[list] = ARRAY(item_type=String(), nullable=True)


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
async def test_filter_array_column_contains(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c"]).save()

    found = await ArrayTestModel.objects.filter(
        (ArrayTestModel.data.array_contains(["c"]))
    ).all()

    assert len(found) == 1
    assert found[0].data == ["c"]


@pytest.mark.asyncio
async def test_filter_array_column_contains_multiple(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c", "d"]).save()

    found = await ArrayTestModel.objects.filter(
        (ArrayTestModel.data.array_contains(["c"]))
    ).all()

    assert len(found) == 1
    assert found[0].data == ["c", "d"]


@pytest.mark.asyncio
async def test_filter_array_column_contained_by(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c"]).save()
    await ArrayTestModel(data=["c", "d"]).save()
    await ArrayTestModel(data=["c", "d", "e"]).save()

    found = await ArrayTestModel.objects.filter(
        (ArrayTestModel.data.array_contained_by(["c", "d"]))
    ).all()

    assert len(found) == 2
    assert found[0].data == ["c"]
    assert found[1].data == ["c", "d"]


@pytest.mark.asyncio
async def test_filter_array_column_overlap(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c"]).save()
    await ArrayTestModel(data=["c", "d"]).save()
    await ArrayTestModel(data=["c", "d", "e"]).save()

    found = await ArrayTestModel.objects.filter(
        (ArrayTestModel.data.array_overlap(["a", "d"]))
    ).all()

    assert len(found) == 3
    assert found[0].data == ["a", "b"]
    assert found[1].data == ["c", "d"]
    assert found[2].data == ["c", "d", "e"]


@pytest.mark.asyncio
async def test_filter_array_column_equals(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c", "d"]).save()

    found = await ArrayTestModel.objects.filter(
        (ArrayTestModel.data == ["c", "d"])
    ).all()

    assert len(found) == 1
    assert found[0].data == ["c", "d"]

    found = await ArrayTestModel.objects.filter((ArrayTestModel.data == ["c"])).all()
    assert len(found) == 0


@pytest.mark.asyncio
async def test_multi_dimensional_array(db):
    await MultiDimensionArrayTestModel(data=[[1, 2], [3, 4]]).save()

    found = await MultiDimensionArrayTestModel.objects.get()
    assert found.data == [
        [1, 2],
        [3, 4],
    ]
