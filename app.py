import os
import json
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
import time

chat_history = []

def parse_retriever_input(params: Dict):
    return params["messages"][-1].content

def add_user_message(user_input):
    new_message = HumanMessage(content=user_input)
    chat_history.append(new_message)

def add_ai_message(ai_response):
    new_message = AIMessage(content=ai_response)
    chat_history.append(new_message)

#TODO: There's a cleaner way to do this. Maybe separate into its own file?
def get_sources(response):

    #Take source and just get the hyphenated part to search the json
    def format_source(source):
        source_name = os.path.basename(source)
        #split at period and take first part
        source_name = source_name.split(".")[0]
        return source_name

    sources = [document.metadata['source'] for document in response["context"]]

    #Make a new list of sources with the hyphenated part
    cleaned_sources = []
    for source in sources:
        cleaned_source = format_source(source)
        cleaned_sources.append(cleaned_source)

    #Now we search the json for the sources
    with open('./map-files-to-links/aaa_all_link_maps.json') as f:
        data = json.load(f)

    #Get the matching keys
    relevant_keys = []
    for source in cleaned_sources:
       for key in data.keys():
           if source in key:
               relevant_keys.append(key)
    
    #Store the values for the matching keys
    relevant_sources = []
    for key in relevant_keys:
        relevant_sources.append(data[key])

    #Now we format for the return. If it's a podcast, return the link.
    #If study notes, return the title and link.
    #If script references, just a string including the title suggesting to search for the video.
    further_info = []
    for source in relevant_sources:
        #TODO: For podcast, need to figure out how to make the link the video title
        #once I get to the frontend
        if "podcast" in source[0]:
            further_info.append(f"Listen to the \"{source[1]}\" podcast located here: {source[0]}")
        elif "study-notes" in source[0]:
            further_info.append(f"See the study notes on \"{source[1]}\", at {source[0]}")
        elif "video" in source[0]:
            further_info.append(f"Search for \"{source[1]}\"{source[0]}")
        else:
            further_info.append("We didn't find a source for this in our mapping. Please report this error.")

    return further_info

#Chat engine
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, max_tokens=450)

#Retriever from Pinecone
index_name = "bible-project-index"
vectorstore = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(k=25)


#RAG answer synthesis prompt
SYSTEM_TEMPLATE = """
You are an assistant designed to help people understand the Bible and the story of Jesus by using content from The Bible Project.
You are cheerful and helpful and love exploring the Bible with people.
Your job is to answer the user's questions based on the below context. 

Some guidelines for your role:
You will not deviate from these guidelines.
If the question is not related to the Bible or Christianity, reply with:
"Hmm. I'm not sure about that. I'm designed to help you understand the Bible and the story of Jesus. Try asking something related to the that!"

If you cannot find information in the provided context, reply with:
"Hmm. I'm not sure about that and I couldn't find enough information in the Bible Project archives. Try rephrasing the question or asking something else."

If somebody asks about your purpose, reply with:
"I'm an assistant designed to help people understand the Bible and the story of Jesus by using content from The Bible Project. I'm cheerful and helpful and love exploring the Bible with people! 😊"

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




def display_chat_history():
    """Displays conversation history in Streamlit chat format"""
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"].replace('\n', '  \n'), unsafe_allow_html=True)

def run_rag_conversation(user_input):
    """Runs RAG conversation and returns AI response with additional sources"""
    add_user_message(user_input)
    response = conversational_retrieval_chain.invoke(
        {
            "messages": chat_history,
        }
    )
    ai_response = response["answer"]
    sources = get_sources(response)
    ai_response += f"\n\nHere's what we'd suggest for further learning: \n" + '\n'.join(sources)
    add_ai_message(ai_response)
    return ai_response

#Lets us stream the response
def response_streamer(response):
    #Streamlit uses html, so need to replace newlines with <br/>
    for word in response.replace('\n', '  \n').split():
        yield word + " "
        time.sleep(0.05)


st.title("Bible Project RAG Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []
display_chat_history()

if prompt := st.chat_input("Ask me a question about the Bible!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Run RAG conversation and get AI response
    response = run_rag_conversation(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.replace('\n', '  \n'), unsafe_allow_html=True)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})