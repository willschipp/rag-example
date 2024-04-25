
import logging
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

DB_FAISS_PATH = 'vectorstore/db_faiss_nomic_full'
# DB_FAISS_PATH = 'vectorstore/db_faiss_nomic_rh_sub'
EMBEDDINGS_MODEL = "nomic-embed-text"
# BASE_URL = "http://localhost:11434"
BASE_URL = "https://hsipo4p3av3f60-11434.proxy.runpod.net"

class Vector:

    embeddings = None
    db = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL,base_url=BASE_URL)
        if os.path.exists(DB_FAISS_PATH):
            self.db = FAISS.load_local(DB_FAISS_PATH,
                                    OllamaEmbeddings(model=EMBEDDINGS_MODEL,base_url=BASE_URL),
                                    allow_dangerous_deserialization=True) #TODO remove
            

    def getRetriever(self,question):
        similarity = self.db.similarity_search(question)
        similarity = FAISS.from_documents(documents=similarity,
                                          embedding=self.embeddings)
        return similarity.as_retriever()
    
    def ingest(self,documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        logging.info("Splitting the documents")
        splits = text_splitter.split_documents(documents)
        logging.info(str(len(documents)) + " " + str(len(splits)))
        logging.info("embedding...")
        starttime = time.time()
        store = FAISS.from_documents(documents=splits,embedding=self.embeddings)
        endtime = time.time()
        logging.info("...complete")
        logging.info(endtime - starttime)
        store.save_local(DB_FAISS_PATH)

