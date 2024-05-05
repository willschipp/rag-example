import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import json
import os
import time


BASE_URL = "http://localhost:11434"
# BASE_URL = "http://34.132.193.18:11434"
EMBED_MODEL = "nomic-embed-text"
COLLECTION = ""

chroma_client = chromadb.PersistentClient("./db")
ef = embedding_functions.OllamaEmbeddingFunction(url=BASE_URL + "/api/embeddings",
                                                        model_name=EMBED_MODEL)
collection = chroma_client.get_or_create_collection(name=COLLECTION,embedding_function=ef)
 
jsons_complete = []


current_count = collection.count()
#load in all the jsons to iterate through
document_count = current_count + 1
# jsons = os.listdir('./json')
for json_file in jsons_complete:
    print(f"starting {json_file}")
    starttime = time.time()
    #structure is content --> content; book --> metadata
    with open("./clean/" + json_file) as file:
        data = json.load(file)
        # its an array
        page = 0
        for item in data:            
            id = str(document_count) + "." + str(page)
            # add to the collection as a document
            if len(item['content']) > 0:
                addstart = time.time()
                try:
                    collection.add(
                        documents=[item['content']],
                        metadatas=[{"source":item['book']}],
                        ids=[id]
                    )
                    addend = time.time()
                    addresult = addend-addstart
                    contentlength = len(item['content'])
                    print(f"page added {page} {contentlength} in {addresult}")
                except Exception as error:
                    print(f"error {error}")
                page += 1
        # break #--> done after one
    endtime = time.time()
    duration = str(endtime - starttime)
    print(f"finished {document_count} {json_file} {duration}")
    
    document_count += 1

