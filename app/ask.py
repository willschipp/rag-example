
import logging
from app.vector import Vector
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

QUESTION_MODEL = "mistral"

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

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.llm = Ollama(model=QUESTION_MODEL)
        self.vector = Vector()
        self.prompt = ChatPromptTemplate.from_template(PROMPT)

    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self,question):
        #get the retriever
        logging.info("getting the context")
        retriever = self.vector.getRetriever(question)
        #build the chain
        rag_chain = (
            {"context": retriever | self.format_docs, "question":RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
            )
        #return the stream
        logging.info("asking the question")
        return rag_chain.stream(question)