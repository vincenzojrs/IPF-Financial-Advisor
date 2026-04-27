from collections import defaultdict
import streamlit as st
from src.engine.orchestrator import invoke_graph
from src.app.rvb_widgets import FormRvb, PMZSelection, render_user_message, render_assistant_response
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
    
if "zona" not in st.session_state:
    st.session_state.zona = None
    
if "zona_submitted" not in st.session_state:
    st.session_state.zona_submitted = False   


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Come posso aiutarti?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = invoke_graph({"query": prompt}, config=st.session_state.orchestrator_config)
    st.session_state.last_response = response
    
    render_assistant_response(response)

if st.session_state.last_response is not None and "__interrupt__" in st.session_state.last_response and st.session_state.last_response["__interrupt__"][0].value["step"] == "Parametri":
    choices = FormRvb()

    if choices.submitted:
        st.session_state.form_submitted = True
        st.session_state.user_input = choices.user_inputs
        render_user_message("Parametri:", choices.user_inputs)

    if st.session_state.form_submitted:
        response = invoke_graph(Command(resume=st.session_state.user_input), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.form_submitted = False
        render_assistant_response(response)

if st.session_state.last_response is not None and "__interrupt__" in st.session_state.last_response and st.session_state.last_response["__interrupt__"][0].value["step"] == "Provincia":
    step = st.session_state.last_response["__interrupt__"][0].value["step"]
    choices = st.session_state.last_response["__interrupt__"][0].value["choices"]

    choice = PMZSelection(step, choices)
    if choice.submitted:
        st.session_state.province_submitted = True
        st.session_state.province = choice.choice
        render_user_message(step, choice.choice)
        
    if st.session_state.province_submitted:
        response = invoke_graph(Command(resume=st.session_state.province), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.province_submitted = False
        render_assistant_response(response)
            
if st.session_state.last_response is not None and "__interrupt__" in st.session_state.last_response and st.session_state.last_response["__interrupt__"][0].value["step"] == "Municipalità":
    step = st.session_state.last_response["__interrupt__"][0].value["step"]
    choices = st.session_state.last_response["__interrupt__"][0].value["choices"]

    choice = PMZSelection(step, choices)
    if choice.submitted:
        st.session_state.municipalità_submitted = True
        st.session_state.municipalità = choice.choice
        render_user_message(step, choice.choice)
        
    if st.session_state.municipalità_submitted:
        response = invoke_graph(Command(resume=st.session_state.municipalità), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.municipalità_submitted = False
        render_assistant_response(response)
            
if st.session_state.last_response is not None and "__interrupt__" in st.session_state.last_response and st.session_state.last_response["__interrupt__"][0].value["step"] == "Zona":
    step = st.session_state.last_response["__interrupt__"][0].value["step"]
    choices = st.session_state.last_response["__interrupt__"][0].value["choices"]

    choice = PMZSelection(step, choices)
    if choice.submitted:
        st.session_state.zona_submitted = True
        st.session_state.zona = choice.choice
        render_user_message(step, choice.choice)
        
    if st.session_state.zona_submitted:
        response = invoke_graph(Command(resume=st.session_state.zona), config=st.session_state.orchestrator_config)
        
        st.session_state.last_response = response
        st.session_state.zona_submitted = False
        render_assistant_response(response)