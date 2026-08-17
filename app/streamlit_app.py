import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.agent.graph import build_graph

st.set_page_config(page_title="Autonomous Research Agent", page_icon="🔎", layout="centered")

st.title("🔎 Autonomous Research Agent")
st.caption("LangGraph + Tavily + OpenRouter — multi-step research with self-critique")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

query = st.text_area("What do you want researched?", height=100, placeholder="e.g. What are the latest developments in AI agent frameworks?")

col1, col2 = st.columns([1, 4])
with col1:
    max_iterations = st.number_input("Max loops", min_value=1, max_value=5, value=2)

run_button = st.button("Run Research", type="primary")

if run_button:
    if not query.strip():
        st.warning("Pehle query likho.")
    else:
        initial_state = {
            "query": query,
            "research_plan": [],
            "search_results": [],
            "sources": [],
            "draft_answer": "",
            "final_answer": "",
            "iteration": 0,
            "max_iterations": max_iterations,
            "needs_more_research": False,
            "session_id": str(uuid.uuid4()),
        }

        with st.spinner("Researching... (planning → searching → synthesizing → checking)"):
            try:
                result = st.session_state.graph.invoke(initial_state)
                answer = result.get("final_answer") or result.get("draft_answer")
                sources = list(dict.fromkeys(result.get("sources", [])))  # dedupe, preserve order

                st.subheader("Answer")
                st.markdown(answer)

                if sources:
                    st.subheader("Sources")
                    for s in sources:
                        if s:
                            st.markdown(f"- [{s}]({s})")

                st.divider()
                if st.button("🔄 New Search"):
                    st.rerun()            

            except Exception as e:
                st.error(f"Error aaya: {e}")


                