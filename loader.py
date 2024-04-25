from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

from app.vector import Vector


def loadDocuments(directory):
    loader = DirectoryLoader(directory,show_progress=True,loader_cls=TextLoader)
    print("loading...")
    docs = loader.load()
    print("...finished")
    # embed
    vector = Vector()
    print("starting to embed")
    vector.ingest(docs)
    print("embedding finished")


def sim_search_test(question):
    vector = Vector()
    answer = vector.db.similarity_search(question)
    print(len(answer))
    for a in answer:
        print(a)
        print("#######")    


if __name__ == "__main__":
    directory = "./data/redhat_docs"
    loadDocuments(directory)
    # sim_search_test("how do I install a single node")