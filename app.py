import os
from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
from dotenv import load_dotenv
import pygame
from gtts import gTTS
from time import time
import threading

# Load API keys
load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize APIs
from google.generativeai import configure, GenerativeModel

configure(api_key=GOOGLE_API_KEY)
model = GenerativeModel('gemini-pro')
pygame.mixer.init()

# Define constants
RECORDING_PATH = "audio/recording.wav"
RESPONSE_PATH = "audio/response.mp3"
PROMPT_TEMPLATE = "You are Lana, Boss human assistant. You are witty and full of personality. Your answers should be limited to 3 lines short sentences.\nBoss: {user_input}\nLana: "

# Initialize Flask app
app = Flask(__name__)
is_listening = False
thread = None
latest_transcription = ""
latest_response = ""
conversation_lock = threading.Lock()

def log(message: str):
    """Print and write to status.txt"""
    print(message)
    with open("status.txt", "a") as f:
        f.write(message + "\n")

def request_gemini(prompt: str) -> str:
    """Generate content using the Gemini model"""
    response = model.generate_content(prompt)
    return response.text

def transcribe_audio() -> str:
    """Transcribe audio using Google's speech recognition"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(RECORDING_PATH) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        log("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        log(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def record_audio() -> str:
    """Record audio using speech_recognition"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        log("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    with open(RECORDING_PATH, "wb") as f:
        f.write(audio.get_wav_data())
    log("Done recording")
    return "Recording complete"

def listen_and_respond():
    global is_listening, latest_transcription, latest_response
    while is_listening:
        try:
            # Record audio
            record_audio()

            # Transcribe audio
            words = transcribe_audio()
            if not words:
                continue

            # Update latest transcription immediately
            with conversation_lock:
                latest_transcription = words

            # Get response from Gemini
            prompt = PROMPT_TEMPLATE.format(user_input=words)
            response = request_gemini(prompt)

            # Update latest response immediately
            with conversation_lock:
                latest_response = response

            # Convert response to audio and play it
            tts = gTTS(response)
            tts.save(RESPONSE_PATH)
            sound = pygame.mixer.Sound(RESPONSE_PATH)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))

        except Exception as e:
            log(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_listening', methods=['POST'])
def start_listening():
    global is_listening, thread, latest_transcription, latest_response
    if not is_listening:
        is_listening = True
        latest_transcription = ""
        latest_response = ""
        thread = threading.Thread(target=listen_and_respond)
        thread.start()
        return jsonify({"status": "success", "message": "Listening started"})
    else:
        return jsonify({"status": "error", "message": "Already listening"})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    global is_listening
    is_listening = False
    return jsonify({"status": "success", "message": "Listening stopped"})

@app.route('/process_audio', methods=['POST'])
def process_audio():
    global latest_transcription, latest_response
    with conversation_lock:
        if latest_transcription or latest_response:
            response = {
                "status": "success",
                "user_transcript": latest_transcription,
                "response": latest_response
            }
            latest_transcription = ""
            latest_response = ""
            return jsonify(response)
    return jsonify({"status": "error", "message": "No new transcription available"})

if __name__ == '__main__':
    app.run(debug=True)