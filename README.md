# 🔎 Autonomous Research Agent

A multi-step research agent built with **LangGraph** that plans, searches, synthesizes, and critiques its own answers — looping back for more research when its own output is incomplete.

Given a query, the agent doesn't just do a single search-and-answer. It breaks the query into sub-questions, researches each one, drafts an answer, checks its own work, and iterates if needed — a small, self-correcting research loop rather than a single LLM call.

---

## How It Works

```
        ┌───────────┐
        │  Planner  │  breaks query into sub-questions
        └─────┬─────┘
              ▼
        ┌───────────┐
   ┌───▶│  Search   │  Tavily search per sub-question
   │    └─────┬─────┘
   │          ▼
   │    ┌───────────┐
   │    │ Synthesize│  drafts an answer from search results
   │    └─────┬─────┘
   │          ▼
   │    ┌───────────┐
   └────│ Critique  │  checks if the draft is complete
        └─────┬─────┘
              ▼
        Final Answer + Sources
```

- **Planner** — breaks the query into 1–5 focused sub-questions, scaled to the query's complexity
- **Search** — runs a Tavily web search for each sub-question
- **Synthesize** — drafts a coherent, cited answer from all search results
- **Critique** — decides if the draft is complete; if not, loops back to Search (bounded by a max-iterations limit to avoid infinite loops)

This graph-based, stateful loop is built with **LangGraph**, which manages the state (query, plan, search results, sources, draft, iteration count) across every node.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | Gemini 2.5 Flash, via [OpenRouter](https://openrouter.ai) |
| Web search | [Tavily](https://tavily.com) |
| UI | [Streamlit](https://streamlit.io) |
| Memory / persistence | [Supabase](https://supabase.com) *(in progress)* |

The LLM is swappable — it's called through `ChatOpenAI` pointed at OpenRouter's endpoint, so any OpenRouter-supported model (Claude, GPT, Gemini, Llama, etc.) can be dropped in by changing one line in `src/agent/nodes.py`.

---

## Demo

*(screenshot/GIF coming soon)*

---

## Project Structure

```
autonomous-research-agent/
├── src/
│   ├── agent/
│   │   ├── state.py       # shared state schema across the graph
│   │   ├── prompts.py     # planner / synthesis / critique prompts
│   │   ├── nodes.py       # node functions (planner, search, synthesize, critique)
│   │   └── graph.py       # LangGraph wiring — the loop itself
│   ├── memory/             # Supabase session persistence (in progress)
│   └── tools/              # search tool wrappers
├── app/
│   └── streamlit_app.py   # web UI
├── requirements.txt
└── .env.example
```

---

## Running It Locally

**1. Clone and set up a virtual environment**
```bash
git clone https://github.com/shahzadsarwar123/autonomous-research-agent.git
cd autonomous-research-agent
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate   # macOS/Linux
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Copy `.env.example` to `.env` and fill in your keys:
```
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
TAVILY_API_KEY=your-tavily-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
```

- Tavily key: [tavily.com](https://tavily.com) (free tier available)
- OpenRouter key: [openrouter.ai](https://openrouter.ai)
- Supabase URL/key: from your Supabase project's API settings

**4. Run the agent**

CLI test:
```bash
python -m src.agent.graph
```

Web UI:
```bash
streamlit run app/streamlit_app.py
```

---

## Design Notes

- **Bounded loops** — the critique → search loop is capped by a `max_iterations` setting to prevent runaway API usage while still allowing the agent to self-correct.
- **Query-proportional depth** — prompts are written so a simple factual query gets a concise answer, and a complex multi-part query gets a fuller one, instead of always maxing out response length.
- **Provider-agnostic LLM layer** — routing through OpenRouter means the agent isn't locked into one model provider.

## Roadmap

- [x] Core LangGraph pipeline (plan → search → synthesize → critique loop)
- [x] Streamlit UI
- [ ] Supabase session memory (save/retrieve past research)
- [ ] Deployment (EC2)
- [ ] LangSmith tracing for observability

---

Built as part of a portfolio demonstrating production-style agentic AI system design — multi-step planning, tool use, self-critique loops, and state management with LangGraph.