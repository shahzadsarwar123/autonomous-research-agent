from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    # user input
    query: str

    # planning
    research_plan: List[str]          # list of sub-questions to research

    # search results
    search_results: Annotated[List[dict], operator.add]  # accumulates across nodes
    sources: Annotated[List[str], operator.add]           # URLs collected

    # synthesis
    draft_answer: str
    final_answer: str

    # control flow
    iteration: int
    max_iterations: int
    needs_more_research: bool

    # metadata
    session_id: str