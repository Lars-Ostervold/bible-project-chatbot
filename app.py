import streamlit as st
import openai
import os
from dotenv import load_dotenv
load_dotenv()

#RAG
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, max_tokens=150)
index_name = "bible-project-index"

vectorstore = PineconeVectorStore(index_name=index_name, embedding=OpenAIEmbeddings())


retriever = vectorstore.as_retriever(k=4)

docs = retriever.invoke("What is the Bible Project?")

print(docs)



from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_TEMPLATE = """
Answer the user's questions based on the below context. 
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

<context>
{context}
</context>
"""












#----Let's worry about streamlit later-------
# st.set_page_config(page_title="Chat with the Podcast Bot", page_icon="🎙️", layout="centered", initial_sidebar_state="auto", menu_items=None)

# st.title("Chat with the Podcast Bot 🎙️")
# st.info("Ask me a question about my favorite podcast!")

# if "messages" not in st.session_state.keys(): # Initialize the chat messages history
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Ask me a question about my favorite podcast!"}
#     ]

# @st.cache_resource(show_spinner=False)
# def load_data():
#     with st.spinner(text="Loading and indexing the podcast data – hang tight! This should take 1-2 minutes."):
#         # Load your data into Pinecone here
#         # index = pinecone.load_data(...)
#         return index

# index = load_data()

# if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
#     # Use Langchain to initialize your chat engine here
#     # st.session_state.chat_engine = langchain.initialize_chat_engine(...)

# if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

# for message in st.session_state.messages: # Display the prior chat messages
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # If last message is not from assistant, generate a new response
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             # Use Langchain and Pinecone to generate a response here
#             # response = st.session_state.chat_engine.chat(prompt)
#             st.write(response)
#             message = {"role": "assistant", "content": response}
#             st.session_state.messages.append(message) # Add response to message history