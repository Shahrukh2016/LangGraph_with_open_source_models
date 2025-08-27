import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

st.title("💬 Chat Me Now! - AI Assistant")
## ---------------------------------------------------------------------- UTILITY FUNCTIONS ------------------------------------------------------------------------------------------------------------------

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_threads(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

## ---------------------------------------------------------------------- SESSION SETUP ------------------------------------------------------------------------------------------------------------------
# message_history = []               ## We cant use the normal empty list to print the conversation history, as it reinitiates everytime when the code updates.

## We can use streamlit session state that stores the conversational history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_threads(st.session_state['thread_id'])

## ---------------------------------------------------------------------- SIDEBAR UI ------------------------------------------------------------------------------------------------------------------

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('Past Conversations')

for thread_id in st.session_state['chat_threads']:
    st.sidebar.button(str(thread_id))

## ---------------------------------------------------------------------- MAIN UI ------------------------------------------------------------------------------------------------------------------
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type here")

if user_input:
    # First add the user message to message history
    st.session_state['message_history'].append({'role' : 'user', 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)


    # Second add the assistant message to message history
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                       {'messages': [HumanMessage(content= user_input)]},
                       config= CONFIG,
                       stream_mode= 'messages'
                       )
                    )
    st.session_state['message_history'].append({'role' : 'assistant', 'content' : ai_message})

    
