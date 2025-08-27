import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# message_history = []               ## We cant use the normal empty list to print the conversation history, as it reinitiates everytime when the code updates.

## We can use streamlit session state that stores the conversational history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type here")

if user_input:
    # First add the user message to message history
    st.session_state['message_history'].append({'role' : 'user', 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

    ai_message = response['messages'][-1].content
    # Second add the assistant message to message history
    st.session_state['message_history'].append({'role' : 'assistant', 'content' : ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
