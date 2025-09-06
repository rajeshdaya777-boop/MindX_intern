import azure.cognitiveservices.speech as speechsdk
import openai
import os
import json
import glob
import csv
import difflib
from dotenv import load_dotenv

load_dotenv()

# Azure credentials
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-05-01-preview"
deployment_id = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

def recognize_speech():
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print("Speak into your microphone...")
        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized:", result.text)
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"Canceled: {cancellation.reason}")
            if cancellation.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation.error_details}")
        return None
    except Exception as e:
        print("Error in speech recognition:", str(e))
        return None

def generate_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            engine=deployment_id,
            messages=[
                {"role": "system", "content": "You are a helpful FAQ assistant. Your responses should be concise and informative. Use the knowledge base information when available: {knowledge_base_context}"},
                {"role": "user", "content": user_input}
            ]
        )
        print(response)
        reply = response['choices'][0]['message']['content']
        print("Bot:", reply)
        return reply
    except Exception as e:
        print("Error generating response:", str(e))
        return "Sorry, I'm facing issues responding right now."

def speak_text(text):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        synthesizer.speak_text_async(text).get()
    except Exception as e:
        print("Error in text-to-speech:", str(e))


def load_knowledge_base(directory="knowledge_base"):
    knowledge_base = {}

    try:
        # Load JSON files
        json_files = glob.glob(f"{directory}/*.json")
        for jf in json_files:
            try:
                with open(jf, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        knowledge_base.update(data)
            except Exception as e:
                print(f"Error loading JSON file {jf}: {e}")

        # Load TXT files
        txt_files = glob.glob(f"{directory}/*.txt")
        for tf in txt_files:
            try:
                with open(tf, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    # Store text content under a special key or append to a list
                    knowledge_base[f"TextFile:{os.path.basename(tf)}"] = content
            except Exception as e:
                print(f"Error loading TXT file {tf}: {e}")

        # Load CSV files
        csv_files = glob.glob(f"{directory}/*.csv")
        for cf in csv_files:
            try:
                with open(cf, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 2:
                            question = row[0].strip()
                            answer = row[1].strip()
                            knowledge_base[question] = answer
            except Exception as e:
                print(f"Error loading CSV file {cf}: {e}")

    except Exception as e:
        print("Error loading knowledge base:", str(e))

    return knowledge_base


def find_answer(faq, question):
    # Use fuzzy matching to find closest question in FAQ
    questions = list(faq.keys())
    matches = difflib.get_close_matches(question, questions, n=1, cutoff=0.6)
    if matches:
        matched_question = matches[0]
        return faq[matched_question]
    return None

def main():
    import time
    faq = load_knowledge_base("/knowledge_base")
    greeting = "Hello! I am your FAQ chatbot. What would you like to know? You can say 'exit' anytime to quit."
    print(greeting)
    speak_text(greeting)

    last_input_time = time.time()
    timeout_seconds = 15

    while True:
        user_query = recognize_speech()
        current_time = time.time()

        if user_query:
            last_input_time = current_time
            if user_query.strip().lower() == "exit":
                exit_msg = "Goodbye! Exiting now."
                print(exit_msg)
                speak_text(exit_msg)
                break

            answer = find_answer(faq, user_query)
            if answer:
                print("Answer found in knowledge base.")
                speak_text(answer)
            else:
                print("Answer not found in knowledge base, using AI model.")
                reply = generate_response(user_query)
                speak_text(reply)
        else:
            if current_time - last_input_time > timeout_seconds:
                no_input_msg = "I didn't hear anything for a while. Exiting now."
                print(no_input_msg)
                speak_text(no_input_msg)
                break
            else:
                # Prompt user again to speak
                prompt_msg = "I didn't hear anything. Please say something or say 'exit' to quit."
                print(prompt_msg)
                speak_text(prompt_msg)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Thank you!")
