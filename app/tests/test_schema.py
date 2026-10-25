
from pprint import pprint

from app.db.schema import discover_schema


if __name__ == "__main__":
    schema = discover_schema()

    if schema:
        pprint(schema, sort_dicts=False)
    else:
        print("No tables found in the public schema.")
