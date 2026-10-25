from app.agent.graph import analyst_graph


def test_graph_compiles():
    """Check that the LangGraph workflow is compiled."""
    assert analyst_graph is not None


def test_graph_has_expected_nodes():
    """Check that all four workflow nodes exist."""
    graph = analyst_graph.get_graph()

    expected_nodes = {
        "generate_sql",
        "validate_sql",
        "execute_sql",
        "generate_answer",
    }

    actual_nodes = set(graph.nodes.keys())

    assert expected_nodes.issubset(actual_nodes)


def test_graph_stops_when_sql_generation_fails(monkeypatch):
    """Check that the graph stops when SQL generation fails."""
    from app.agent import nodes

    def fake_generate_sql(question: str) -> str:
        raise RuntimeError("Test SQL generation error")

    monkeypatch.setattr(nodes, "generate_sql", fake_generate_sql)

    result = analyst_graph.invoke({
        "question": "Test question",
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "error": "",
        "retry_count": 0,
        "truncated": False,
    })

    assert result["error"] == "SQL generation failed: Test SQL generation error"


def test_graph_stops_when_sql_validation_fails(monkeypatch):
    """Check that invalid SQL is rejected before execution."""
    from app.agent import nodes

    def fake_generate_sql(question: str) -> str:
        return "DROP TABLE customers"

    monkeypatch.setattr(nodes, "generate_sql", fake_generate_sql)

    result = analyst_graph.invoke({
        "question": "Delete the customers table",
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "error": "",
        "retry_count": 0,
        "truncated": False,
    })

    assert "Only SELECT queries are allowed" in result["error"]


def test_graph_stops_when_sql_execution_fails(monkeypatch):
    """Check that the graph stops when SQL execution fails."""
    from app.agent import nodes

    def fake_generate_sql(question: str) -> str:
        return "SELECT 1"

    def fake_execute_query(query: str) -> dict:
        raise RuntimeError("Test database error")

    monkeypatch.setattr(nodes, "generate_sql", fake_generate_sql)
    monkeypatch.setattr(
        nodes, "execute_read_only_query", fake_execute_query
    )

    result = analyst_graph.invoke({
        "question": "Test question",
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "error": "",
        "retry_count": 0,
        "truncated": False,
    })

    assert result["error"] == "Test database error"
    assert result.get("answer", "") == ""


def test_graph_handles_answer_generation_failure(monkeypatch):
    """Check that answer-generation errors are captured."""
    from app.agent import nodes

    def fake_generate_sql(question: str) -> str:
        return "SELECT 1 AS number"

    def fake_execute_query(query: str) -> dict:
        return {
            "columns": ["number"],
            "rows": [{"number": 1}],
            "row_count": 1,
            "truncated": False,
        }

    def fake_generate_answer(**kwargs) -> str:
        raise RuntimeError("Test answer generation error")

    monkeypatch.setattr(nodes, "generate_sql", fake_generate_sql)
    monkeypatch.setattr(
        nodes, "execute_read_only_query", fake_execute_query
    )
    monkeypatch.setattr(
        nodes, "generate_answer", fake_generate_answer
    )

    result = analyst_graph.invoke({
        "question": "What is the number?",
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "error": "",
        "retry_count": 0,
        "truncated": False,
    })

    assert result["error"] == "Test answer generation error"


def test_agent_retries_after_sql_execution_failure(monkeypatch):
    from app.agent import nodes
    from app.agent.graph import analyst_graph

    attempts = {"count": 0}

    def fake_generate_sql(question):
        return "SELECT customer_id FROM customers"

    def fake_execute_sql(query):
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise RuntimeError("Temporary database error")

        return {
            "columns": ["customer_id"],
            "rows": [{"customer_id": 1}],
            "row_count": 1,
            "truncated": False,
        }

    def fake_generate_answer(question, sql, columns, rows):
        return "Customer ID 1"

    monkeypatch.setattr(nodes, "generate_sql", fake_generate_sql)
    monkeypatch.setattr(nodes, "execute_read_only_query", fake_execute_sql)
    monkeypatch.setattr(nodes, "generate_answer", fake_generate_answer)

    result = analyst_graph.invoke({
        "question": "Find a customer",
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "error": "",
        "retry_count": 0,
        "retry_error": "",
        "truncated": False,
    })

    assert attempts["count"] == 3
    assert result["retry_count"] == 2
    assert result["answer"] == "Customer ID 1"
