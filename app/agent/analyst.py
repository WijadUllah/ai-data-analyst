
from app.agent.graph import analyst_graph


def analyze_question(question: str) -> dict:
    """Analyze a business question using the LangGraph workflow."""

    # Step 1: Validate the user's question.
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 2: Prepare the initial graph state.
    initial_state = {
        "question": question,
        "sql": "",
        "columns": [],
        "rows": [],
        "answer": "",
        "error": "",
        "retry_count": 0,
        "truncated": False,
    }

    # Step 3: Run the LangGraph workflow.
    result = analyst_graph.invoke(initial_state)

    # Step 4: Handle workflow errors.
    if result.get("error"):
        raise ValueError(f"Analysis failed: {result['error']}")

    # Step 5: Return the complete response.
    return {
        "question": question,
        "sql": result["sql"],
        "answer": result["answer"],
        "columns": result["columns"],
        "rows": result["rows"],
        "row_count": len(result["rows"]),
        "truncated": result.get("truncated", False),
    }
