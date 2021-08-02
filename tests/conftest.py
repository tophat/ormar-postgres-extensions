import pytest
import sqlalchemy

from .database import (
    DATABASE_URL,
    DB_NAME,
    database,
    metadata,
)


@pytest.fixture()
def root_engine():
    root_engine = sqlalchemy.create_engine(
        str(DATABASE_URL.replace(database="postgres")), isolation_level="AUTOCOMMIT"
    )
    return root_engine


@pytest.fixture()
def test_database(root_engine):
    with root_engine.connect() as conn:
        print(f"Creating test database '{DB_NAME}'")
        conn.execute(f'DROP DATABASE IF EXISTS "{DB_NAME}";')
        conn.execute(f'CREATE DATABASE "{DB_NAME}"')

    yield

    with root_engine.connect() as conn:
        root_engine.execute(f'DROP DATABASE "{DB_NAME}"')


@pytest.fixture()
async def db(test_database):
    # Ensure the DB has the schema we need for testing
    engine = sqlalchemy.create_engine(str(DATABASE_URL))
    metadata.create_all(engine)
    engine.dispose()

    await database.connect()
    yield
    await database.disconnect()
