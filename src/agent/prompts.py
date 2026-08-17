PLANNER_PROMPT = """You are a research planning assistant. Given a user's research query, break it down into 3-5 specific, focused sub-questions that together would fully answer the original query.

Return ONLY a numbered list of sub-questions, nothing else.

Query: {query}
"""

SYNTHESIS_PROMPT = """You are a research synthesis assistant. Given the original query and search results below, write a comprehensive, well-structured answer.

Cite sources where relevant using [Source: URL] format.

Original Query: {query}

Search Results:
{search_results}

Write a clear, well-organized answer:
"""

CRITIQUE_PROMPT = """You are a research quality checker. Given the original query and the draft answer below, decide if the answer is complete and accurate enough, or if more research is needed.

Original Query: {query}

Draft Answer:
{draft_answer}

Respond with ONLY one word: "COMPLETE" or "INCOMPLETE"
"""