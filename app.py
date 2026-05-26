from collections import defaultdict
import streamlit as st
from src.engine.orchestrator import invoke_graph
from src.app.widgets import FormRvb, PMZSelection
from src.app.functions import render_user_message, render_assistant_response
from langgraph.types import Command

st.title("Il financial advisor per pignolazzi!")
st.info("""
             Poni qualunque domanda all'agente Pignolazzi.
             
             Prova con "che cos'è un'azione?" o "a cosa serve un'obbligazione": ti risponderà attingendo alla conoscenza di Italia Personal Finance.
             
             Inoltre, ha anche a disposizione un tool a cui potrà ricorrere se gli chiedi informazioni relative alla convenienza dell acquisto di una casa.
             """,
             icon="ℹ️")

# Define variables to be persistent across reruns

# config is necessary to work with interrupts
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

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check existence of prompt
if prompt := st.chat_input("Come posso aiutarti?"):
    
    # Append the prompt in the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the last message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Invoke the graph using the prompt
    response = invoke_graph({"query": prompt}, config=st.session_state.orchestrator_config)
    
    # Make response persistent across reruns
    st.session_state.last_response = response
    
    # Render response
    render_assistant_response(response)

# Check which interrupt; if interrupt is "Parameteri"
if st.session_state.last_response is not None and "__interrupt__" in st.session_state.last_response and st.session_state.last_response["__interrupt__"][0].value["step"] == "Parametri":
    
    # Display input form
    choices = FormRvb()

    # If form submitted
    if choices.submitted:
        
        # Returns a peristent variable saying "I clicked on submit in the previous run"
        st.session_state.form_submitted = True
        
        # Make user input persistent
        st.session_state.user_input = choices.user_inputs
        
        # Render user input
        render_user_message("Parametri:", choices.user_inputs)

    # If in the previous run the user clicked on submit
    if st.session_state.form_submitted:
        # Pass the user inputs in the graph
        response = invoke_graph(Command(resume=st.session_state.user_input), config=st.session_state.orchestrator_config)
        
        # Make the response persistent
        st.session_state.last_response = response
        
        # Returns a peristent variable saying "I did not click on submit in the previous run"
        st.session_state.form_submitted = False
        
        # Render output
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