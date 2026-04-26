from collections import defaultdict
import streamlit as st
from src.engine.orchestrator import invoke_graph
from src.app.rvb_frontend import FormRvb, PMZSelection
from langgraph.types import Command

st.title("Il financial advisor per pignolazzi!")

if "orchestrator_config" not in st.session_state:
    st.session_state.orchestrator_config = {
        "configurable": {
            "thread_id" : "1"
        }
    }

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "user_input" not in st.session_state:
    st.session_state.user_input = None

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
    
if "province" not in st.session_state:
    st.session_state.province = None
    
if "province_submitted" not in st.session_state:
    st.session_state.province_submitted = False
    
if "municipalità" not in st.session_state:
    st.session_state.municipalità = None
    
if "municipalità_submitted" not in st.session_state:
    st.session_state.municipalità_submitted = False


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Come posso aiutarti?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = invoke_graph({"query": prompt}, config=st.session_state.orchestrator_config)
    st.session_state.last_response = response

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.last_response is not None and st.session_state.last_response["__interrupt__"][0].value["step"] == "human_input":
    form = FormRvb()

    if form.submitted:
        st.session_state.form_submitted = True
        st.session_state.user_input = form.user_inputs

    if st.session_state.form_submitted:
        response = invoke_graph(Command(resume=st.session_state.user_input), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.form_submitted = False
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)

if st.session_state.last_response is not None and st.session_state.last_response["__interrupt__"][0].value["step"] == "provincia":
    step = st.session_state.last_response["__interrupt__"][0].value["step"]
    choices = st.session_state.last_response["__interrupt__"][0].value["choices"]

    choice = PMZSelection(step, choices)
    if choice.submitted:
        st.session_state.province_submitted = True
        st.session_state.province = choice.choice
        
    if st.session_state.province_submitted:
        response = invoke_graph(Command(resume=st.session_state.province), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.province_submitted = False
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)
            
if st.session_state.last_response is not None and st.session_state.last_response["__interrupt__"][0].value["step"] == "municipalità":
    step = st.session_state.last_response["__interrupt__"][0].value["step"]
    choices = st.session_state.last_response["__interrupt__"][0].value["choices"]

    choice = PMZSelection(step, choices)
    if choice.submitted:
        st.session_state.municipalità_submitted = True
        st.session_state.municipalità = choice.choice
        
    if st.session_state.municipalità_submitted:
        response = invoke_graph(Command(resume=st.session_state.municipalità), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.municipalità_submitted = False
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)
            
if st.session_state.last_response is not None and st.session_state.last_response["__interrupt__"][0].value["step"] == "zona":
    step = st.session_state.last_response["__interrupt__"][0].value["step"]
    choices = st.session_state.last_response["__interrupt__"][0].value["choices"]

    choice = PMZSelection(step, choices)
    if choice.submitted:
        st.session_state.municipalità_submitted = True
        st.session_state.municipalità = choice.choice
        
    if st.session_state.municipalità_submitted:
        response = invoke_graph(Command(resume=st.session_state.municipalità), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.municipalità_submitted = False
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)