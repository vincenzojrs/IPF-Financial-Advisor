import streamlit as st
from main import FinancialAdvisorRAG

st.title("Il financial advisor per pignolazzi!")

rag = FinancialAdvisorRAG()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Come posso aiutarti?"):
    st.session_state.messages.append({"role" : "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)