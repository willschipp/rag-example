import chromadb
import chromadb.utils.embedding_functions as embedding_functions

import ollama
import time

PROMPT = '''
    Answer the question using the context only.
    Context: {context}
    Question: {question}
'''

BASE_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
COLLECTION = ""

chroma_client = chromadb.PersistentClient("./db")
ef = embedding_functions.OllamaEmbeddingFunction(url=BASE_URL + "/api/embeddings",
                                                        model_name=EMBED_MODEL)
collection = chroma_client.get_or_create_collection(name=COLLECTION,embedding_function=ef)

question = ""

print("searching...")
starttime = time.time()
results = collection.query(
    query_texts=[question],
    n_results=10
)
endtime = time.time()
print(endtime - starttime)
#documents is an array of arrays
documents = results['documents']
context = []
for document in documents:
    for d in document:
        context.append(d)

prompt = PROMPT.format(context=context,question=question)
print("asking ai...")
starttime = time.time()
response = ollama.generate(model="mistral",prompt=prompt)
print(response['response'])
endtime = time.time()
print(endtime - starttime)

