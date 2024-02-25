import os
from operator import itemgetter
from typing import List, Tuple, Dict
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    format_document,
)
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import streamlit as st

chat_history = []

def parse_retriever_input(params: Dict):
    return params["messages"][-1].content

def add_user_message(user_input):
    new_message = HumanMessage(content=user_input)
    chat_history.append(new_message)

def add_ai_message(ai_response):
    new_message = AIMessage(content=ai_response)
    chat_history.append(new_message)

#Chat engine
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, max_tokens=150)

#Retriever from Pinecone
index_name = "bible-project-index"
vectorstore = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(k=4)


#RAG answer synthesis prompt
SYSTEM_TEMPLATE = """
Answer the user's questions based on the below context. 
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

<context>
{context}
</context>
"""

question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_TEMPLATE,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

#Not really sure what document_chain does? TODO: Read up on this
document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

#Retrieval chain
retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever,
).assign(
    answer=document_chain,
)

#Query transformation chain to rephrase as single query
query_transform_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else.",
        ),
    ]
)

query_transformation_chain = query_transform_prompt | chat

query_transforming_retriever_chain = RunnableBranch(
    (
        lambda x: len(x.get("messages", [])) == 1,
        # If only one message, then we just pass that message's content to retriever
        (lambda x: x["messages"][-1].content) | retriever,
    ),
    # If messages, then we pass inputs to LLM chain to transform the query, then pass to retriever
    query_transform_prompt | chat | StrOutputParser() | retriever,
).with_config(run_name="chat_retriever_chain")

conversational_retrieval_chain = RunnablePassthrough.assign(
    context=query_transforming_retriever_chain,
).assign(
    answer=document_chain,
)


#Set up a 10x loop for testing
for i in range(10):
    #User input
    user_input = input("You: ")
    add_user_message(user_input)

    response = conversational_retrieval_chain.invoke(
        {
            "messages": chat_history,
        }
    )

    ai_response = response["answer"]
    add_ai_message(ai_response)
    print("AI: ", ai_response)


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