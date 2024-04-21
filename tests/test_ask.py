import unittest

from app.ask import Ask
from langchain.docstore.document import Document

class Testing(unittest.TestCase):

    def test_format_docs(self):
        #create a doc
        doc_0 = Document(page_content="hello",metadata={"source":"test"})
        doc_1 = Document(page_content="world",metadata={"source":"test"})
        docs = [doc_0,doc_1]
        #format it
        ask = Ask()
        result = ask.format_docs(docs)
        lines = result.splitlines()
        self.assertTrue(len(lines) == 3)
        