import streamlit as st

st.header("PDF Helper")

text = '''
*PDF Helper* enables you to upload and search through PDFs

### How it works

Go to the 'Upload' page and upload your PDF.  Once complete, go to the 'Query' page to ask question of that document.

### Proof of Concept

This is a RAG design Proof of Concept to identify key architectural components
'''

st.markdown(text)