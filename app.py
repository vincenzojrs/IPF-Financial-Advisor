import streamlit as st
from main import FinancialAdvisorRAG
from collections import defaultdict

st.title("Il financial advisor per pignolazzi!")

def render_citations(citations):
    with st.expander("Queste sono le fonti che ho utilizzato:"):
        grouped = defaultdict(list)
        for citation in citations:
            grouped[citation["source_url"]].append(citation["id"])
        for url, ids in grouped.items():
            st.markdown(f"{', '.join(ids)} : {url}")

if "rag" not in st.session_state:
    st.session_state.rag = FinancialAdvisorRAG()

# Initiate chat history, if not exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and "citations" in message:
            render_citations(message["citations"])

# Create chat input bar, and append prompt to chat history
if prompt := st.chat_input("Come posso aiutarti?"):
    st.session_state.messages.append({"role" : "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.rag.ask(prompt)
        st.markdown(response.answer)
        citations = [c.model_dump() for c in response.citations]
        render_citations(citations)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.answer,
        "citations": citations
    })