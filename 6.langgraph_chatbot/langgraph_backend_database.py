from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_perplexity import ChatPerplexity
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

## Defining and initiating model
model = ChatPerplexity(model= 'sonar', api_key= os.getenv("PERPLEXITY_API_KEY"))

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

## Initiating SQL DB
conn = sqlite3.connect(database= 'chatbot.db', check_same_thread= False)

# Checkpointer
checkpointer = SqliteSaver(conn= conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)