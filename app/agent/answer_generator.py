
import json

from langchain_groq import ChatGroq

from app.config import settings


def generate_answer(
    question: str,
    sql: str,
    columns: list,
    rows: list,
) -> str:
    """Explain database query results in simple business language."""

    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    if not rows:
        return "No matching records were found in the database."

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
        max_retries=2,
    )

    results_json = json.dumps(
        {
            "columns": columns,
            "rows": rows,
        },
        indent=2,
        default=str,
    )

    prompt = f"""
You are a business data analyst explaining database results to a CEO.

Answer the CEO's question using only the supplied query results.

Rules:
1. Be clear, concise, and professional.
2. Never invent facts, numbers, or business insights.
3. Do not claim that the results show more than they actually show.
4. If the results are insufficient to answer the question,
   explain the limitation.
5. If multiple rows show the same highest value, mention the tie
   only when all relevant tied rows are present.
6. Do not execute SQL or suggest that you executed another query.
7. Format monetary amounts clearly when the currency is known.
   Do not assume a currency if it is not specified.

CEO question:
{question}

SQL used:
{sql}

Database results:
{results_json}

Write the answer for the CEO:
"""

    response = llm.invoke(prompt)
    answer = response.content

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("The model returned an empty answer.")

    return answer.strip()
