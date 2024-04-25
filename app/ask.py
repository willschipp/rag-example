
import logging
from app.vector import Vector
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

QUESTION_MODEL = "mistral"
QUESTION_MODEL_LLAMA_2 = "llama2"
QUESTION_MODEL_LLAMA_3 = "llama3"

# BASE_URL = "http://localhost:11434"
BASE_URL = "https://hsipo4p3av3f60-11434.proxy.runpod.net/"


PROMPT = """Answer the following question based only on the provided context:
        <context>
        {context}
        </context>
        question = {question}
        If the answer is not in the website answer "I'm not sure what you are asking about."
        ALWAYS return a "SOURCES" part in your answer.
        """


class Ask:

    llm = None
    vector = None
    prompt = None
    model_name = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        # self.llm = Ollama(model=QUESTION_MODEL,base_url=BASE_URL)
        self.vector = Vector()
        self.prompt = ChatPromptTemplate.from_template(PROMPT)

    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self,question):
        #get the retriever
        logging.info("getting the context")
        retriever = self.vector.getRetriever(question)
        logging.info(self.model_name)
        llm = Ollama(model=self.model_name,base_url=BASE_URL)
        #build the chain
        rag_chain = (
            {"context": retriever | self.format_docs, "question":RunnablePassthrough()}
            | self.prompt
            | llm
            | StrOutputParser()
            )
        #return the stream
        logging.info("asking the question")
        return rag_chain.stream(question)
    
    def change_model(self,model):
        # if model == 'llama2:70b':
        #     self.model_name = 'llama2:70b'
        # elif model == 'llama3:70b':
        #     self.model_name = 'llama3:70b'
        # else:
        self.model_name = model