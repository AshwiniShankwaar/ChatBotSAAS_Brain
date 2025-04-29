from Brain.DataLoader.DocumentLoader import DocumentLoader # Import the class
from Brain.DataLoader.WebLoader import WebLoader # Import the class
import os
from Brain.text_splitter.json_text_splitter import json_text_splitter
from Brain.text_splitter.char_text_splitter import char_text_splitter


if __name__ == '__main__':
    #load document
    #test for pdf loader
    loader = DocumentLoader("./files/concepts.pdf")
    # loader = WebLoader("https://python.langchain.com/docs",True,2)
    doc = loader.load()
    # print(len(doc))

    #perform text_split
    # splitter = json_text_splitter(doc)
    splitter = char_text_splitter(doc)
    chunks = splitter.processDocumnet()
    print(len(chunks))
    pass

