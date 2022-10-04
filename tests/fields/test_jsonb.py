import json
from typing import Optional

import ormar
import pytest
from sqlalchemy.dialects.postgresql import array

import ormar_postgres_extensions as ormar_pg_ext
from tests.database import (
    database,
    metadata,
)


class JSONBTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: dict = ormar_pg_ext.JSONB()


class NullableJSONBTestModel(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    data: Optional[dict] = ormar_pg_ext.JSONB(nullable=True)


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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value1, value2, value3",
    [
        # Test with some JSON primitives
        ("value1", "value2", "value3"),
        (1, 2, 3),
        (True, False, None),
        # Verifies that matches with NULL work
        (True, None, False),
    ],
)
async def test_contains(db, value1, value2, value3):
    await JSONBTestModel(data=json.dumps(dict(key=value1))).save()
    await JSONBTestModel(data=json.dumps(dict(key=value2))).save()

    found = await JSONBTestModel.objects.filter(
        data__jsonb_contains=dict(key=value2)
    ).all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(
        data__jsonb_contains=dict(key=value3)
    ).all()
    assert len(found) == 0


@pytest.mark.asyncio
async def test_contains_array(db):
    await JSONBTestModel(data=json.dumps([1, 2])).save()
    await JSONBTestModel(data=json.dumps([1, 3])).save()

    found = await JSONBTestModel.objects.filter(data__jsonb_contains=[1]).all()
    assert len(found) == 2

    found = await JSONBTestModel.objects.filter(data__jsonb_contains=[1, 2]).all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(data__jsonb_contains=[4]).all()
    assert len(found) == 0


@pytest.mark.asyncio
async def test_contains_array_text(db):
    await JSONBTestModel(data=json.dumps([1, 2])).save()
    await JSONBTestModel(data=json.dumps([1, 3])).save()

    found = await JSONBTestModel.objects.filter(data__jsonb_contains="1").all()
    assert len(found) == 2

    found = await JSONBTestModel.objects.filter(data__jsonb_contains="4").all()
    assert len(found) == 0


@pytest.mark.asyncio
async def test_contained_by(db):
    await JSONBTestModel(data=json.dumps(dict(key1="foo"))).save()
    await JSONBTestModel(data=json.dumps(dict(key2="bar"))).save()

    found = await JSONBTestModel.objects.filter(
        data__jsonb_contained_by=dict(key1="foo")
    ).all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(
        data__jsonb_contained_by=dict(key1="foo", key2="bar")
    ).all()
    assert len(found) == 2

    found = await JSONBTestModel.objects.filter(
        data__jsonb_contains=dict(key1="bar")
    ).all()
    assert len(found) == 0


@pytest.mark.asyncio
async def test_has_all(db):
    await JSONBTestModel(data=json.dumps(dict(key1="foo", key3=2))).save()
    await JSONBTestModel(data=json.dumps(dict(key2="bar"))).save()

    found = await JSONBTestModel.objects.filter(
        data__jsonb_has_all=array(["key1"])
    ).all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(
        data__jsonb_has_all=array(["key1", "key2"])
    ).all()
    assert len(found) == 0

    found = await JSONBTestModel.objects.filter(
        data__jsonb_has_all=array(["key1", "key3"])
    ).all()
    assert len(found) == 1


@pytest.mark.asyncio
async def test_has_any(db):
    await JSONBTestModel(data=json.dumps(dict(key1="foo", key3=2))).save()
    await JSONBTestModel(data=json.dumps(dict(key2="bar"))).save()

    found = await JSONBTestModel.objects.filter(
        data__jsonb_has_any=array(["key1"])
    ).all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(
        data__jsonb_has_any=array(["key1", "key3"])
    ).all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(
        data__jsonb_has_any=array(["key1", "key2"])
    ).all()
    assert len(found) == 2


@pytest.mark.asyncio
async def test_has_key_object(db):
    await JSONBTestModel(data=json.dumps(dict(key1="foo"))).save()
    await JSONBTestModel(data=json.dumps(dict(key2="bar"))).save()

    found = await JSONBTestModel.objects.filter(data__jsonb_has_key="key1").all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(data__jsonb_has_key="key3").all()
    assert len(found) == 0


@pytest.mark.asyncio
async def test_has_key_array(db):
    await JSONBTestModel(data=json.dumps(["foo"])).save()
    await JSONBTestModel(data=json.dumps(["bar"])).save()

    found = await JSONBTestModel.objects.filter(data__jsonb_has_key="foo").all()
    assert len(found) == 1

    found = await JSONBTestModel.objects.filter(data__jsonb_has_key="other").all()
    assert len(found) == 0
