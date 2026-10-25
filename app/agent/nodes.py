from app.agent.state import AnalystState
from app.agent.sql_generator import generate_sql

from app.db.query_executor import (
    validate_sql,
    execute_read_only_query,
)
from app.agent.answer_generator import generate_answer


def generate_sql_node(state: AnalystState) -> dict:
    """Generate SQL from the user's question."""
    try:
        question = state["question"]
        retry_error = state.get("retry_error", "")

        if retry_error:
            question = (
                f"{question}\n\n"
                f"The previous SQL attempt failed with this error:\n"
                f"{retry_error}\n"
                "Generate corrected PostgreSQL SQL. "
                "Use only tables and columns in the database schema."
            )

        generated_sql = generate_sql(question)

        return {
            "sql": generated_sql,
            "error": "",
        }

    except Exception as exc:
        return {
            "error": f"SQL generation failed: {exc}",
        }




def validate_sql_node(state: AnalystState) -> dict:
    """Validate the generated SQL before execution."""

    try:
        safe_sql = validate_sql(state["sql"])

        return {
            "sql": safe_sql,
            "error": "",
        }

    except ValueError as exc:
        return {
            "error": str(exc),
        }



def execute_sql_node(state: AnalystState) -> dict:
    """Execute validated SQL and store the results."""
    try:
        result = execute_read_only_query(state["sql"])
        return {
            "columns": result["columns"],
            "rows": result["rows"],
            "error": "",
            "truncated": result["truncated"],
        }
    except Exception as exc:
        return {"error": str(exc)}




def generate_answer_node(state: AnalystState) -> dict:
    """Generate a natural-language answer from query results."""

    try:
        answer = generate_answer(
            question=state["question"],
            sql=state["sql"],
            columns=state["columns"],
            rows=state["rows"],
        )

        return {
            "answer": answer,
            "error": "",
        }

    except Exception as exc:
        return {
            "error": str(exc),
        }


def prepare_sql_retry_node(state: AnalystState) -> dict:
    """Prepare state for another SQL-generation attempt."""

    return {
        "retry_error": state.get("error", ""),
        "retry_count": state.get("retry_count", 0) + 1,
        "error": "",
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "truncated": False,
    }
