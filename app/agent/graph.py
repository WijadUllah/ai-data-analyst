
from langgraph.graph import StateGraph, START, END

from app.agent.state import AnalystState
from app.agent.nodes import (
    generate_sql_node,
    validate_sql_node,
    execute_sql_node,
    generate_answer_node,
    prepare_sql_retry_node,
)

MAX_RETRIES = 2

def route_after_generation(state: AnalystState) -> str:
    """Stop if SQL generation fails."""
    if state.get("error"):
        return "error"
    return "validate_sql"


def route_after_validation(state: AnalystState) -> str:
    """Retry if SQL validation fails and retries remain."""
    if not state.get("error"):
        return "execute_sql"

    if state.get("retry_count", 0) < MAX_RETRIES:
        return "retry"

    return "error"


def route_after_execution(state: AnalystState) -> str:
    """Retry if SQL execution fails and retries remain."""
    if not state.get("error"):
        return "generate_answer"

    if state.get("retry_count", 0) < MAX_RETRIES:
        return "retry"

    return "error"


builder = StateGraph(AnalystState)

builder.add_node("generate_sql", generate_sql_node)
builder.add_node("validate_sql", validate_sql_node)
builder.add_node("execute_sql", execute_sql_node)
builder.add_node("generate_answer", generate_answer_node)
builder.add_node("prepare_sql_retry", prepare_sql_retry_node)

builder.add_edge(START, "generate_sql")
builder.add_conditional_edges(
    "generate_sql",
    route_after_generation,
    {
        "validate_sql": "validate_sql",
        "error": END,
    },
)

builder.add_conditional_edges(
    "validate_sql",
    route_after_validation,
    {
        "execute_sql": "execute_sql",
        "retry": "prepare_sql_retry",
        "error": END,
    },
)

builder.add_conditional_edges(
    "execute_sql",
    route_after_execution,
    {
        "generate_answer": "generate_answer",
        "retry": "prepare_sql_retry",
        "error": END,
    },
)

builder.add_edge("prepare_sql_retry", "generate_sql")

analyst_graph = builder.compile()
