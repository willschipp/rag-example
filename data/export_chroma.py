import chromadb
import json
# import chromadb.utils.embedding_functions as embedding_functions

BASE_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
COLLECTION = "homeopathy"

#client
chroma_client = chromadb.PersistentClient("./db")

# ef = embedding_functions.OllamaEmbeddingFunction(url=BASE_URL + "/api/embeddings",
#                                                         model_name=EMBED_MODEL)
collection = chroma_client.get_collection(name=COLLECTION)

documents = collection.get()

rows = []
ids = documents["ids"]
for id in ids:
    #get the record and dump to json
    row = collection.get(id,include=['embeddings','documents','metadatas'])
    rows.append(row)

with open("./dump.json","w") as file:
    json.dump(rows,file,indent=6)
