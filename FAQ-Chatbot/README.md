### MindX

# FAQ Chatbot with Azure OpenAI and Streamlit

A friendly FAQ chatbot built with Streamlit and Microsoft Azure OpenAI API that provides context-aware responses based on a custom knowledge base.

## Features

- 🤖 Interactive chat interface with Streamlit
- 📚 Multi-format knowledge base support (Excel, CSV, JSON, PDF, DOCX, TXT)
- 🔍 Semantic search using FAISS
- 💬 Context-aware conversation history
- 🎯 Azure OpenAI GPT-4 integration
- 🎨 Modern and user-friendly UI

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and fill in your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name_here
   ```
4. Add your knowledge base files to the `knowledge_base` folder:
   - Supported formats: Excel (.xlsx, .xls), CSV (.csv), JSON (.json), PDF (.pdf), Word (.docx), Text (.txt)
   - For structured data (Excel, CSV, JSON), use the following formats:
     - Excel/CSV: Two columns named "Question" and "Answer"
     - JSON: Array of objects with "question" and "answer" fields
   - For unstructured data (PDF, DOCX, TXT), the content will be automatically chunked and indexed

## Running the Application

To start the chatbot, run:
```bash
streamlit run app.py
```

## Usage

1. The chatbot will greet you with a welcome message
2. Type your question in the chat input
3. The bot will respond based on the knowledge base
4. Use the sidebar to:
   - View chat history
   - Clear the conversation
   - Start a new chat
5. Click "End Chat" to receive a goodbye message

## Knowledge Base Formats

### Structured Data Formats

1. Excel/CSV Format:
   ```
   Question,Answer
   What services do you offer?,We offer a range of services...
   How can I contact support?,You can reach our support team...
   ```

2. JSON Format:
   ```json
   [
     {
       "question": "What services do you offer?",
       "answer": "We offer a range of services..."
     },
     {
       "question": "How can I contact support?",
       "answer": "You can reach our support team..."
     }
   ]
   ```

### Unstructured Data Formats

- PDF, DOCX, and TXT files will be automatically:
  - Extracted and processed
  - Split into manageable chunks
  - Indexed for semantic search
  - Used to answer relevant questions

## Customization

- Add or modify files in the `knowledge_base` folder to update the knowledge base
- Adjust the response style by modifying the system prompt in `app.py`
- Customize the UI by modifying the Streamlit components
- Modify the chunk size in `process_text_content()` for different text processing granularity

## Note

Make sure you have valid Azure OpenAI credentials and an active deployment before running the application.
=======

