from sqlalchemy import inspect
from app.db.connection import engine


def discover_schema() -> dict:
    inspector = inspect(engine)

    schema_info = {}

    # Discover tables in the public schema
    tables = inspector.get_table_names(schema="public")

    for table_name in tables:
        columns = inspector.get_columns(
            table_name,
            schema="public",
        )

        foreign_keys = inspector.get_foreign_keys(
            table_name,
            schema="public",
        )

        schema_info[table_name] = {
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                }
                for column in columns
            ],
            "foreign_keys": foreign_keys,
        }

    return schema_info
