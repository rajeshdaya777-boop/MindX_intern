# Conversational FAQ Chatbot with Azure Speech and OpenAI

## Overview

`main.py` is a conversational FAQ chatbot that uses Azure Cognitive Services for speech recognition and synthesis, and OpenAI's GPT model for generating responses. The chatbot listens to user speech input, answers questions based on a provided knowledge base, and speaks the answers back to the user. It supports multiple knowledge base file types including JSON, TXT, and CSV.

## Features

- Speech-to-text using Azure Speech SDK.
- Text-to-speech using Azure Speech SDK.
- Conversational loop with greeting and continuous interaction.
- Knowledge base loading from multiple file types (JSON, TXT, CSV) in a specified directory.
- Fuzzy matching to find the closest FAQ answer.
- Fallback to OpenAI GPT model for questions not found in the knowledge base.
- Exit on user command "exit" or after 15 seconds of silence.

## Setup

1. Clone the repository or copy the files to your local machine.

2. Install required Python packages:

```bash
pip install azure-cognitiveservices-speech openai python-dotenv
```

3. Prepare your environment variables in a `.env` file or system environment:

```
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_speech_region
AZURE_OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
AZURE_OPENAI_DEPLOYMENT_ID=your_openai_deployment_id
```

4. Prepare your knowledge base files in a directory (default is `/knowledge_base`):

- JSON files with question-answer pairs.
- TXT files with text content.
- CSV files with two columns: question, answer.

## Usage

Run the chatbot script:

```bash
python main.py
```

Speak into your microphone when prompted. Say "exit" to quit the chatbot. If no speech is detected for 15 seconds, the chatbot will exit automatically.

## Code Structure

- `recognize_speech()`: Captures speech input from the microphone.
- `speak_text(text)`: Converts text to speech and plays it.
- `load_knowledge_base(directory)`: Loads and combines knowledge base files from the specified directory.
- `find_answer(faq, question)`: Finds the closest matching answer from the knowledge base using fuzzy matching.
- `generate_response(user_input)`: Calls OpenAI GPT to generate a response if no knowledge base match is found.
- `main()`: Main conversational loop handling user interaction.

## Notes

- Ensure your microphone is properly configured and accessible.
- The chatbot requires internet access for OpenAI API calls.
- Customize the knowledge base directory path in the code if needed.

## License

This project is provided as-is without warranty. Use at your own risk.
