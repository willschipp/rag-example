import streamlit as st
from app.ask import Ask

st.header("Ask questions of the PDF")
query = st.text_input("Enter your question here")

ask = Ask()

if (query):
    with st.spinner("Asking model..."):
        response = ask.ask(query)
        st.write_stream(response)
    