import unittest

import pdf_to_text as processor

class test_pdf_to_text(unittest.TestCase):

    # def test_extract_text(self):
    #     pdf = "./book1.pdf"
    #     results = processor.extract_text(pdf)
    #     self.assertTrue(len(results) > 0)

    # def test_embed(self):
        #get the pages
        # pdf = "./book1.pdf"
        # pages = processor.extract_text(pdf)    

        # pages = []
        # page = {"number":1,
        #         "content":"hello world"}
        # pages.append(page)    
        #embed
        # processor.embed(pages)

    # def test_dump_pages(self):
    #     #get the pages
    #     pdf = "./book1.pdf"
    #     pages = processor.extract_text(pdf)        
    #     #dump
    #     processor.dump_pages(pages)

    def test_dump_clean_pages(self):
        #get the pages
        pdf = "./book1.pdf"
        pages = processor.extract_text(pdf)        
        #clean
        pages = processor.clean_text(pages)
        #dump
        processor.dump_pages(pages)                

