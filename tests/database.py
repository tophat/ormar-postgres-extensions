import databases
import sqlalchemy

DB_HOST = "localhost"
DB_NAME = "TEST_DATABASE"
DATABASE_URL = databases.DatabaseURL(
    f"postgres://DEV_USER:DEV_PASSWORD@{DB_HOST}:5432/{DB_NAME}"
)
database = databases.Database(str(DATABASE_URL))
metadata = sqlalchemy.MetaData()
