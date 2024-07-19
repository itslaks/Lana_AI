# Lana_AI

Lana_AI is an interactive AI assistant that uses speech recognition and natural language processing to engage in conversation with users. It combines the power of Google's Speech Recognition, Gemini AI model, and text-to-speech technology to create a seamless voice-based interaction experience.

## Features

- Voice-activated AI assistant
- Real-time speech recognition
- Natural language processing using Google's Gemini AI model
- Text-to-speech response generation
- Interactive web interface

## Technology Stack

- Python 3.x
- Flask (Web framework)
- SpeechRecognition (Google Speech Recognition API)
- Google Gemini AI (Natural Language Processing)
- gTTS (Google Text-to-Speech)
- PyGame (Audio playback)
- HTML/CSS/JavaScript (Frontend)
- Particles.js (Background animation)

## Setup and Installation

1. Clone the repository:
git clone https://github.com/itslaks/Lana_AI.git
cd Lana_AI

2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install the required packages:
pip install flask python-dotenv pygame gTTS SpeechRecognition google-generativeai

  
4. Set up your environment variables:
Create a `.env` file in the project root and add your Google API key:
GEMINI_API_KEY=your_api_key_here

  
5. Run the application:
python app.py

6. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Click the microphone button to start listening.
2. Speak your query or command.
3. Lana will process your speech, generate a response, and speak it back to you.
4. The conversation will be displayed in the chat interface.
5. Click the microphone button again to stop listening.

## Project Structure

- `app.py`: Main Flask application file containing the server-side logic.
- `templates/index.html`: HTML template for the web interface.
- `audio/`: Directory to store temporary audio files.
- `status.txt`: Log file for debugging purposes.

## Development Process

1. Set up the basic Flask application structure.
2. Implemented speech recognition using Google's Speech Recognition API.
3. Integrated Google's Gemini AI model for natural language processing.
4. Added text-to-speech functionality using gTTS.
5. Developed the frontend interface with HTML, CSS, and JavaScript.
6. Implemented real-time communication between frontend and backend.
7. Added background animation using Particles.js.
8. Optimized the conversation flow and error handling.

## Future Improvements

- Implement user authentication for personalized experiences.
- Add support for multiple languages.
- Improve error handling and recovery mechanisms.
- Optimize performance for faster response times.
- Implement a database to store conversation history.

## Contributing

Contributions to Lana_AI are welcome! Please feel free to submit a Pull Request.



## Acknowledgments

- Google Speech Recognition API
- Google Gemini AI
- Particles.js library
