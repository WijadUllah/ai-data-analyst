
import sqlglot
from sqlglot import exp
from sqlalchemy import text

from app.db.connection import engine


MAX_ROWS = 100
STATEMENT_TIMEOUT_MS = 5000

BLOCKED_FUNCTIONS = {
    "pg_sleep",
    "pg_read_file",
    "pg_read_binary_file",
    "pg_ls_dir",
    "pg_stat_file",
    "lo_import",
    "lo_export",
    "dblink",
    "set_config",
    "nextval",
    "setval",
}

def validate_sql(query: str) -> str:
    """Allow one read-only query with no embedded write operations."""

    if not query or not query.strip():
        raise ValueError("SQL query cannot be empty.")

    try:
        statements = sqlglot.parse(query, read="postgres")
    except sqlglot.errors.ParseError as exc:
        raise ValueError("Invalid SQL syntax.") from exc

    # Allow exactly one non-empty statement.
    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Only one SQL statement is allowed.")

    statement = statements[0]

    # Allow SELECT queries, including CTEs.
    if not isinstance(statement, exp.Select):
        raise ValueError("Only SELECT queries are allowed.")

    # Reject SELECT INTO.
    if statement.args.get("into") is not None:
        raise ValueError("SELECT INTO is not allowed.")

    # Reject write or administrative operations anywhere in the AST.
    forbidden_operations = {
        "insert",
        "update",
        "delete",
        "merge",
        "create",
        "drop",
        "alter",
        "truncate",
        "command",
        "copy",
        "grant",
        "revoke",
        "transaction",
        "commit",
        "rollback",
        "set",
        "use",
    }

    for node in statement.walk():
        if node.key.lower() in forbidden_operations:
            raise ValueError(
                f"Forbidden SQL operation detected: {node.key}"
            )

    # ADD THE NEW BLOCK HERE
    for node in statement.walk():
        if isinstance(node, exp.Func):
            function_name = node.name.lower()

            if function_name in BLOCKED_FUNCTIONS:
                raise ValueError(
                    f"Forbidden SQL function: {function_name}"
                )

    return query.strip().rstrip(";").strip()

def execute_read_only_query(query: str) -> dict:
    """Validate SQL and return a limited number of result rows."""

    safe_query = validate_sql(query)

    with engine.connect() as connection:
        with connection.begin():
            # Make this transaction read-only.
            connection.exec_driver_sql("SET TRANSACTION READ ONLY")

            # Stop queries that run too long.
            connection.exec_driver_sql(
                f"SET LOCAL statement_timeout = {STATEMENT_TIMEOUT_MS}"
            )

            result = connection.execute(text(safe_query))

            columns = list(result.keys())
            rows = result.mappings().fetchmany(MAX_ROWS + 1)

            truncated = len(rows) > MAX_ROWS
            rows = rows[:MAX_ROWS]

            return {
                "columns": columns,
                "rows": [dict(row) for row in rows],
                "row_count": len(rows),
                "truncated": truncated,
            }
