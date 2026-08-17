import os
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

from src.agent.state import ResearchState
from src.agent.prompts import PLANNER_PROMPT, SYNTHESIS_PROMPT, CRITIQUE_PROMPT

load_dotenv()

llm = ChatOpenAI(
    model="google/gemini-2.5-flash",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    max_tokens=2000,
)

search_tool = TavilySearch(max_results=5, tavily_api_key=os.getenv("TAVILY_API_KEY"))


def planner_node(state: ResearchState) -> dict:
    """Break the query into sub-questions."""
    prompt = PLANNER_PROMPT.format(query=state["query"])
    response = llm.invoke(prompt)
    plan = [line.strip() for line in response.content.split("\n") if line.strip()]
    return {"research_plan": plan}


def search_node(state: ResearchState) -> dict:
    """Run Tavily search for each sub-question in the plan."""
    all_results = []
    all_sources = []

    for question in state["research_plan"]:
        results = search_tool.invoke({"query": question})
        for r in results.get("results", []):
            all_results.append({"question": question, "content": r.get("content", ""), "url": r.get("url", "")})
            all_sources.append(r.get("url", ""))

    return {"search_results": all_results, "sources": all_sources}


def synthesis_node(state: ResearchState) -> dict:
    """Synthesize search results into a draft answer."""
    formatted_results = "\n\n".join(
        [f"Q: {r['question']}\nContent: {r['content']}\nSource: {r['url']}" for r in state["search_results"]]
    )
    prompt = SYNTHESIS_PROMPT.format(query=state["query"], search_results=formatted_results)
    response = llm.invoke(prompt)
    return {"draft_answer": response.content}


def critique_node(state: ResearchState) -> dict:
    """Check if the draft answer is complete."""
    prompt = CRITIQUE_PROMPT.format(query=state["query"], draft_answer=state["draft_answer"])
    response = llm.invoke(prompt)
    is_complete = "COMPLETE" in response.content.upper()

    return {
        "needs_more_research": not is_complete,
        "iteration": state["iteration"] + 1,
        "final_answer": state["draft_answer"] if is_complete else "",
    }