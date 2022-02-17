from typing import Optional

import ormar
import pytest
import sqlalchemy

import ormar_postgres_extensions as ormar_pg_ext
from tests.database import (
    database,
    metadata,
)


class ArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: list = ormar_pg_ext.ARRAY(item_type=sqlalchemy.String())
    thing: str = ormar.String(max_length=20, nullable=True)


class MultiDimensionArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: list = ormar_pg_ext.ARRAY(item_type=sqlalchemy.Integer(), dimensions=2)


class NullableArrayTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: Optional[list] = ormar_pg_ext.ARRAY(
        item_type=sqlalchemy.String(), nullable=True
    )


@pytest.mark.asyncio
async def test_create_model_with_array(db):
    created = await ArrayTestModel(data=["a", "b"], thing="test thing").save()
    assert created.data == ["a", "b"]

    # Confirm the model got saved to the DB by querying it back
    found = await ArrayTestModel.objects.get()
    assert found.data == ["a", "b"]
    assert found.thing == "test thing"


@pytest.mark.asyncio
async def test_create_model_with_nullable_array(db):
    created = await NullableArrayTestModel().save()
    assert created.data is None

    found = await NullableArrayTestModel.objects.get()
    assert found.data is None


@pytest.mark.asyncio
async def test_filter_array_column_contains(db):
    await ArrayTestModel(data=["a", "b"], thing="test thing 2").save()
    await ArrayTestModel(data=["c"]).save()

    found = await ArrayTestModel.objects.filter(data__array_contains=["c"]).all()

    assert len(found) == 1
    assert found[0].data == ["c"]

    found = await ArrayTestModel.objects.filter(thing="test thing 2").all()
    assert len(found) == 1
    assert found[0].data == ["a", "b"]


@pytest.mark.asyncio
async def test_filter_array_column_contains_multiple(db):
    await ArrayTestModel(data=["a", "b"]).save()
    await ArrayTestModel(data=["c", "d"], thing="test thing 2").save()

    found = await ArrayTestModel.objects.filter(data__array_contains=["a"]).all()

    assert len(found) == 1
    assert found[0].data == ["a", "b"]

    found = await ArrayTestModel.objects.filter(
        data__array_contains=["c"], thing="test thing 2"
    ).all()

    assert len(found) == 1
    assert found[0].data == ["c", "d"]


@pytest.mark.asyncio
async def test_filter_array_column_contained_by(db):
    await ArrayTestModel(data=["a", "b"], thing="aa").save()
    await ArrayTestModel(data=["c"]).save()
    await ArrayTestModel(data=["c", "d"], thing="aa").save()
    await ArrayTestModel(data=["c", "d", "e"]).save()

    found = await ArrayTestModel.objects.filter(
        data__array_contained_by=["c", "d"]
    ).all()

    assert len(found) == 2
    assert found[0].data == ["c"]
    assert found[1].data == ["c", "d"]

    found = await ArrayTestModel.objects.filter(
        data__array_contained_by=["c", "d"], thing="aa"
    ).all()

    assert len(found) == 1
    assert found[0].data == ["c", "d"]


@pytest.mark.asyncio
async def test_filter_array_column_overlap(db):
    await ArrayTestModel(data=["a", "b"], thing="aa").save()
    await ArrayTestModel(data=["c"], thing="aa").save()
    await ArrayTestModel(data=["c", "d"], thing="cc").save()
    await ArrayTestModel(data=["c", "d", "e"], thing="aa").save()

    found = await ArrayTestModel.objects.filter(data__array_overlap=["a", "d"]).all()

    assert len(found) == 3
    assert found[0].data == ["a", "b"]
    assert found[1].data == ["c", "d"]
    assert found[2].data == ["c", "d", "e"]

    found = await ArrayTestModel.objects.filter(
        data__array_overlap=["a", "d"], thing="aa"
    ).all()

    assert len(found) == 2
    assert found[0].data == ["a", "b"]
    assert found[1].data == ["c", "d", "e"]


@pytest.mark.asyncio
async def test_filter_array_column_equals(db):
    await ArrayTestModel(data=["a", "b"], thing="aa").save()
    await ArrayTestModel(data=["c", "d"]).save()

    found = await ArrayTestModel.objects.filter(data=["c", "d"]).all()

    assert len(found) == 1
    assert found[0].data == ["c", "d"]

    found = await ArrayTestModel.objects.filter(data=["c"]).all()
    assert len(found) == 0

    found = await ArrayTestModel.objects.filter(data=["c", "d"], thing="aa").all()

    assert len(found) == 0

    found = await ArrayTestModel.objects.filter(data=["a", "b"], thing="aa").all()

    assert len(found) == 1
    assert found[0].data == ["a", "b"]
    assert found[0].thing == "aa"

    found = await ArrayTestModel.objects.filter(thing="aa").all()

    assert len(found) == 1
    assert found[0].data == ["a", "b"]
    assert found[0].thing == "aa"


@pytest.mark.asyncio
async def test_multi_dimensional_array(db):
    await MultiDimensionArrayTestModel(data=[[1, 2], [3, 4]]).save()

    found = await MultiDimensionArrayTestModel.objects.get()
    assert found.data == [
        [1, 2],
        [3, 4],
    ]
