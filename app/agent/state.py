
from typing import TypedDict, Any


class AnalystState(TypedDict):
    question: str
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    answer: str
    error: str
    retry_count: int
    retry_error: str
    truncated: bool
