
import traceback
from pprint import pprint

from app.agent.analyst import analyze_question


if __name__ == "__main__":
    question = "Which product has the highest total quantity sold?"
    try:
        result = analyze_question(question)
        pprint(result, sort_dicts=False)

    except Exception:
        traceback.print_exc()
