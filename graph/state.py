# graph/state.py
from typing import TypedDict

class GraphState(TypedDict):
    question: str
    search_results: str
    scraped_content: str
    outline: list[str]
    final_answer: str



