# Alwrity RAG Chatbot

### Overview

The `alwrity_rag_chatbot.py` module combines functionalities of both a history chatbot and a document question-answering chatbot, providing a comprehensive solution for engaging in conversation with AI and querying information from local documents.

### Key Features

- **History Chatbot**: Save and load past conversation history, allowing users to continue previous chats seamlessly.
- **Document QA Chatbot**: Query information from local documents, PDFs, videos, and audio files using AI.
- **Streamlit Integration**: A user-friendly interface to interact with the chatbot and manage chat histories.

### Setup and Installation

#### Prerequisites

- Python 3.6 or higher
- Required packages: `streamlit`, `joblib`, `google.generativeai`, `dotenv`, `llama_index`, `openai`

#### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AJaySi/AI-Writer.git
    cd AI-Writer
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To run the combined chatbot module, execute the following command:

```bash
streamlit run lib/chatbot_custom/alwrity_rag_chatbot.py
```

#### Modes of Operation

1. **History Chatbot**: 
   - This mode allows users to save and load previous chat sessions.
   - The chatbot will display past messages and handle new user inputs, streaming responses from AI.

2. **Document QA Chatbot**: 
   - This mode enables users to query information from various data sources (local docs, PDFs, videos, audio files).
   - The chatbot will load and index documents, allowing users to ask questions and receive AI-generated responses.

#### Example

1. **History Chatbot Mode**:
   - Run the app and select "History Chatbot" from the sidebar.
   - Interact with the chatbot, and it will save the conversation history for future sessions.

2. **Document QA Chatbot Mode**:
   - Run the app and select "Document QA Chatbot" from the sidebar.
   - Choose the data source (e.g., local docs, PDFs) and provide the necessary input (e.g., folder path).
   - Ask questions, and the chatbot will provide responses based on the indexed documents.

### Contributing

We welcome contributions to enhance the functionalities of the `alwrity_rag_chatbot.py` module. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any issues or questions, feel free to open an issue on the [GitHub repository](https://github.com/AJaySi/AI-Writer/issues).

Happy coding!
