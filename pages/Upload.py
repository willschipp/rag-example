import streamlit as st
import tempfile
import pathlib

from langchain_community.document_loaders import PyPDFLoader
from app.vector import Vector

st.write("Document upload page")

upload_file = st.file_uploader("Choose a PDF",type="pdf")

if upload_file is not None:
    #write the file temporarily
    temp_dir = tempfile.TemporaryDirectory()
    uploaded_file_path = pathlib.Path(temp_dir.name) / "File_Provided"

    with open(uploaded_file_path,'wb') as output_temporary_file:
        output_temporary_file.write(upload_file.read())

    with st.spinner("File processing"):
        loader = PyPDFLoader(uploaded_file_path)
        docs = loader.load()
        vector = Vector()
        vector.ingest(docs)        