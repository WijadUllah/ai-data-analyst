
import json

from langchain_groq import ChatGroq

from app.config import settings
from app.db.schema import discover_schema


def generate_sql(question: str) -> str:
    """Generate PostgreSQL SQL from a natural-language question."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    schema = discover_schema()

    if not schema:
        raise ValueError("No database tables were discovered.")

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
        max_retries=2,
    )

    schema_text = json.dumps(schema, indent=2, default=str)

    prompt = f"""
You are a PostgreSQL SQL generator for a business data analyst.

Generate one PostgreSQL SELECT query to answer the user's question.

Rules:
1. Use only tables and columns in the provided schema.
2. Never invent table or column names.
3. Use foreign-key relationships when appropriate.
4. Return SQL only, without Markdown or explanations.
5. Generate exactly one read-only SELECT statement.
6. Never generate data-modifying statements.
7. When calculating sales revenue from order items,
   use quantity multiplied by the recorded unit price.
8. Do not count cancelled orders as completed sales.
9. If the schema cannot answer the question, return:
   SELECT 'INSUFFICIENT_SCHEMA' AS status;
10. When asked for the highest or lowest value, include all
    tied records when possible. Do not use LIMIT 1 if it
    could hide records tied for the maximum or minimum.


Database schema:
{schema_text}

User question:
{question}
"""

    response = llm.invoke(prompt)
    sql = response.content

    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("The model returned an empty SQL query.")

    return sql.strip()
