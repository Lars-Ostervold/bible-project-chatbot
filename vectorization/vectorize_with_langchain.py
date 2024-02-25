'''
This file loops through resources .txt files and uploads them to Pinecone.
It uses the langchain library to split the text into chunks and the langchain_community library to load the text files.
Vectorization happens inside the .from_documents() method of the PineconeVectorStore class.
'''

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load OpenAI embeddings
embeddings = OpenAIEmbeddings()

resources_path = '../resources'
index_name = 'bible-project-index'  # replace with your Pinecone index name

for subfolder in os.listdir(resources_path):
    subfolder_path = os.path.join(resources_path, subfolder)
    
    if os.path.isdir(subfolder_path):
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(subfolder_path, file_name)
                
                # Load the text file
                #Trap in try/except block to handle encoding issues
                try:
                    loader = TextLoader(file_path)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue

                documents = loader.load()

                # Initialize text splitter
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

                # Split the document into chunks
                chunks = text_splitter.split_documents(documents)
                        
                docsearch = PineconeVectorStore.from_documents(documents=chunks, embedding=embeddings, index_name=index_name)