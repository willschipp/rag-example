
# from pypdf import PdfReader
from PyPDF2 import PdfReader
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

import chromadb

import json

from chromadb.utils import embedding_functions

def extract_text(pdf):
    #return a blob of text for the pdf file
    reader = PdfReader(pdf)

    pages = []

    i = 0

    while (i<len(reader.pages)):
        page = reader.pages[i]
        i += 1
        #process the page
        text = page.extract_text()
        pageObj = {"number":i,
                   "content":text}
        pages.append(pageObj)
    
    return pages

def dump_pages(pages):
    with open("./book1.json","w") as write:
        json.dump(pages,write)

def embed(pages):
    #setup the connection
    client = chromadb.PersistentClient(path="../vectorstore/chroma/")
    #setup the function
    embedding_func = embedding_functions.OllamaEmbeddingFunction(model_name="all-minilm",url="http://localhost:11434")
    #collection
    collection = client.create_collection(
        name="homeopathy",
        embedding_function=embedding_func,
        metadata={"hnsw:space":"cosine"},
    )
    #normalize to documents
    documents = []
    numbers = []
    for page in pages:
        documents.append(page['content'])
        numbers.append(page['number'])
    #add
    collection.add(
        documents=documents,
        ids=[f"id{i}" for i in range(len(documents))],
        metadatas=[{"page":n} for n in numbers]        
    )

def clean_text(pages):
    nltk.download('punkt')
    nltk.download('stopwords')
    clean_pages = []
    stop_words = list(stopwords.words('english'))
    for page in pages:
        tokens = word_tokenize(page['content'])
        filtered_text = [word for word in tokens if not word.lower() in stop_words]
        clean_text = [word.lower() for word in filtered_text if word.isalpha()]
        clean_page = {"content":page['content'],
                      "number":page['number'],
                      "clean_text":clean_text}
        clean_pages.append(clean_page)
    return clean_pages        


