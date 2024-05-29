import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Constants
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '👄'
DATA_DIR = 'data/'


def history_chatbot():
	# Ensure the data/ directory exists
	os.makedirs(DATA_DIR, exist_ok=True)
	
	# Generate a new chat ID
	new_chat_id = f'{time.time()}'
	
	# Load past chats if available
	try:
	    past_chats = joblib.load(os.path.join(DATA_DIR, 'past_chats_list'))
	except FileNotFoundError:
	    past_chats = {}
	
	# Sidebar for past chats
	with st.sidebar:
	    st.write('# Past Chats')
	    if 'chat_id' not in st.session_state:
	        st.session_state.chat_id = st.selectbox(
	            label='Pick a past chat',
	            options=[new_chat_id] + list(past_chats.keys()),
	            format_func=lambda x: past_chats.get(x, 'New Chat'),
	            placeholder='_'
	        )
	    else:
	        st.session_state.chat_id = st.selectbox(
	            label='Pick a past chat',
	            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
	            index=1,
	            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
	            placeholder='_'
	        )
	    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
	
	# Load chat history if available
	try:
	    st.session_state.messages = joblib.load(os.path.join(DATA_DIR, f'{st.session_state.chat_id}-st_messages'))
	    st.session_state.gemini_history = joblib.load(os.path.join(DATA_DIR, f'{st.session_state.chat_id}-gemini_messages'))
	    print('Loaded existing chat history')
	except FileNotFoundError:
	    st.session_state.messages = []
	    st.session_state.gemini_history = []
	    print('Initialized new chat history')
	
	# Configure the AI model
	st.session_state.model = genai.GenerativeModel('gemini-pro')
	st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)
	
	# Display past messages
	for message in st.session_state.messages:
	    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
	        st.markdown(message['content'])
	
	# Handle user input
	if prompt := st.chat_input('Ask Alwrity...'):
	    if st.session_state.chat_id not in past_chats:
	        past_chats[st.session_state.chat_id] = st.session_state.chat_title
	        joblib.dump(past_chats, os.path.join(DATA_DIR, 'past_chats_list'))
	
	    # Display and save user message
	    with st.chat_message('user'):
	        st.markdown(prompt)
	    st.session_state.messages.append({'role': 'user', 'content': prompt})
	
	    # Send message to AI and stream the response
	    response = st.session_state.chat.send_message(prompt, stream=True)
	    full_response = ''
	    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
	        message_placeholder = st.empty()
	        for chunk in response:
	            for ch in chunk.text.split(' '):
	                full_response += ch + ' '
	                time.sleep(0.05)
	                message_placeholder.write(full_response + '▌')
	        message_placeholder.write(full_response)
	
	    # Save the AI response
	    st.session_state.messages.append({
	        'role': MODEL_ROLE,
	        'content': full_response,
	        'avatar': AI_AVATAR_ICON
	    })
	    st.session_state.gemini_history = st.session_state.chat.history
	
	    # Persist chat history to disk
	    joblib.dump(st.session_state.messages, os.path.join(DATA_DIR, f'{st.session_state.chat_id}-st_messages'))
	    joblib.dump(st.session_state.gemini_history, os.path.join(DATA_DIR, f'{st.session_state.chat_id}-gemini_messages'))
