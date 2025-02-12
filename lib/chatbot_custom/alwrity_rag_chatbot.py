import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from pathlib import Path

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
load_dotenv(Path("../../.env"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '👄'
DATA_DIR = 'data/'


def initialize_session_state():
    """Initialize the chat message history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about documents from your local files or from the Web."}
        ]


@st.cache_resource(show_spinner=False)
def load_data(input_dir):
    """Load and index documents from the specified directory."""
    with st.spinner("Loading and indexing your docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir=input_dir, recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(
                model="gpt-3.5-turbo",
                temperature=0.5,
                system_prompt=(
                    "You are an expert on content & digital marketing and your job is to answer technical questions."
                    "Assume that all questions are related to provided documents, as context."
                    "Keep your answers technical and based on facts – do not hallucinate features."
                )
            )
        )
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


def display_chat_history():
    """Display the chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def generate_response(prompt, chat_engine):
    """Generate a response from the chat engine and update the chat history."""
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                st.session_state.messages.append({"role": "assistant", "content": response.response})


def history_chatbot():
    """Main function to run the Streamlit app with history chat functionality."""
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


def alwrity_chat_docqa():
    """Main function to run the Streamlit app with document question answering functionality."""
    st.header("Ask Alwrity 💬 📚")
    initialize_session_state()
    option = st.radio(
        "Choose Data Source To Ask From:",
        ("Ask Your Local Docs", "Ask Your PDFs", "Ask Your Videos", "Ask Your Audio Files")
    )

    if option == "Ask Your Local Docs":
        input_dir = st.text_input("Enter the path to the folder:")
        if input_dir:
            st.session_state.input_dir = input_dir

    elif option == "Ask Your PDFs":
        pdf_file = st.file_uploader("Upload a PDF file or enter a URL:", type=["pdf"])
        if pdf_file:
            st.session_state.input_file = pdf_file

    elif option == "Ask Your Videos":
        video_dir = st.text_input("Enter the path to the video folder:")
        if video_dir:
            st.session_state.input_dir = video_dir

    elif option == "Ask Your Audio Files":
        audio_dir = st.text_input("Enter the path to the audio folder:")
        if audio_dir:
            st.session_state.input_dir = audio_dir

    if 'input_dir' in st.session_state:
        index = load_data(st.session_state.input_dir)
        chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
        display_chat_history()
        prompt = st.chat_input("Your question")
        if st.session_state.messages[-1]["role"] != "assistant":
            generate_response(prompt, chat_engine)
    
    elif 'input_file' in st.session_state:
        # Handle PDF file or URL input here
        st.write("Handling PDF file or URL input is not implemented yet.")


def alwrity_rag_chatbot():
    """Main function to run the combined Streamlit app."""
    st.sidebar.title("Alwrity RAG Chatbot")
    app_mode = st.sidebar.selectbox("Choose mode", ["History Chatbot", "Document QA Chatbot"])
    
    if app_mode == "History Chatbot":
        history_chatbot()
    elif app_mode == "Document QA Chatbot":
        alwrity_chat_docqa()


if __name__ == "__main__":
    alwrity_rag_chatbot()
