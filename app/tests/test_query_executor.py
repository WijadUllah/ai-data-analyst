import pytest

from app.db.query_executor import validate_sql


@pytest.mark.parametrize(
    "query",
    [
        "SELECT pg_sleep(30)",
        "SELECT pg_read_file('/etc/passwd')",
        "SELECT nextval('my_sequence')",
        "SELECT set_config('statement_timeout', '0', false)",
    ],
)
def test_validate_sql_rejects_blocked_functions(query):
    with pytest.raises(ValueError, match="Forbidden SQL function"):
        validate_sql(query)


def test_validate_sql_allows_normal_select():
    assert validate_sql("SELECT customer_id FROM customers") == (
        "SELECT customer_id FROM customers"
    )
    
import pytest

from app.db.query_executor import execute_read_only_query


def test_execute_query_rejects_unsafe_sql():
    with pytest.raises(ValueError, match="Only SELECT queries are allowed"):
        execute_read_only_query("DELETE FROM customers")