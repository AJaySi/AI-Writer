import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path("../../.env"))
openai.api_key = os.getenv("OPENAI_API_KEY")


def initialize_session_state():
    """Initialize the chat message history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Ask me a question about documents from {LOCAL_BRAIN_DATA} or from the Web."}
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


def alwrity_chat_docqa():
    """Main function to run the Streamlit app."""
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
