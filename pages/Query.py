import streamlit as st
from app.ask import Ask

ask = Ask()

def handle_change():
    ask.change_model(st.session_state['model'])

st.header("Ask questions of the PDF")
query = st.text_input("Enter your question here")

option = st.selectbox('Please choose a model',
                      ('mistral','llama2','llama3'),
                      on_change=handle_change,
                      key='model')

if (query):
    with st.spinner("Asking model..."):
        response = ask.ask(query)
        st.write_stream(response)
    