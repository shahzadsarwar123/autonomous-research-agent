from langgraph.graph import StateGraph, END

from src.agent.state import ResearchState
from src.agent.nodes import planner_node, search_node, synthesis_node, critique_node


def should_continue(state: ResearchState) -> str:
    """Decide whether to loop back for more research or finish."""
    if state["needs_more_research"] and state["iteration"] < state["max_iterations"]:
        return "search"
    return "end"


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("synthesize", synthesis_node)
    graph.add_node("critique", critique_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "search")
    graph.add_edge("search", "synthesize")
    graph.add_edge("synthesize", "critique")

    graph.add_conditional_edges(
        "critique",
        should_continue,
        {
            "search": "search",   # loop back if incomplete
            "end": END,
        },
    )

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    initial_state = {
        "query": "What are the latest developments in AI agent frameworks in 2026?",
        "research_plan": [],
        "search_results": [],
        "sources": [],
        "draft_answer": "",
        "final_answer": "",
        "iteration": 0,
        "max_iterations": 2,
        "needs_more_research": False,
        "session_id": "test-session-1",
    }

    result = app.invoke(initial_state)
    print("\n--- FINAL ANSWER ---\n")
    print(result["final_answer"] or result["draft_answer"])
    print("\n--- SOURCES ---\n")
    print(result["sources"])