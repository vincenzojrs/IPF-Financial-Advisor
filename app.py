from collections import defaultdict

import streamlit as st

from src.engine.orchestrator import Graph
from src.app.rvb_frontend import FormRvb
from langgraph.types import Command


st.title("Il financial advisor per pignolazzi!")


if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Graph()
    st.session_state.orchestrator_config = { "configurable": 
                                                {
                                                    "thread_id" : 1
                                                }
                                            }

# Initiate chat history, if not exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create chat input bar, and append prompt to chat history
if prompt := st.chat_input("Come posso aiutarti?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.orchestrator.invoke({"query": prompt}, config = st.session_state.orchestrator_config)
    if response["route"] == "mutuo" and "interrupt" in response:
        form = FormRvb()
        st.session_state.orchestrator.invoke(Command(resume = form.user_inputs), config = st.session_state.orchestrator_config)
        st.session_state.orchestrator.invoke(Command(resume = 'NAPOLI'), config = st.session_state.orchestrator_config)
        st.session_state.orchestrator.invoke(Command(resume = 'NAPOLI'), config = st.session_state.orchestrator_config)
    else:
        answer = response.get("answer")
        with st.chat_message("assistant"):
            st.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
