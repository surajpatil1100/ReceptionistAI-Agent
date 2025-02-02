import os
import csv
from datetime import datetime, timedelta
from vosk import Model, KaldiRecognizer
import pyaudio
from transformers import pipeline
from gtts import gTTS

# Paths
VOSK_MODEL_PATH = "data/vosk_hindi_model/vosk-model-small-hi-0.22"
APPOINTMENTS_FILE = "data/appointments.csv"
AUDIO_FILE = "audio/response.mp3"

# Initialize Vosk model
if not os.path.exists(VOSK_MODEL_PATH):
    print("Error: Vosk Hindi model not found. Please download and place it in the 'data/vosk_hindi_model' folder.")
    exit()

model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Initialize microphone
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Initialize NLP pipeline
nlp = pipeline("text-generation", model="ai4bharat/IndicBART")

# Functions
def listen():
    print("Listening...")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return result

def generate_response(prompt):
    response = nlp(prompt, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

def speak(text):
    tts = gTTS(text=text, lang='hi')
    tts.save(AUDIO_FILE)
    os.system(f"mpg321 {AUDIO_FILE}")  # Play the audio (requires mpg321)

def suggest_time_slots():
    time_slots = [
        datetime.now() + timedelta(hours=1),
        datetime.now() + timedelta(hours=3),
        datetime.now() + timedelta(days=1)
    ]
    return [slot.strftime("%Y-%m-%d %H:%M") for slot in time_slots]

def save_appointment(name, problem, doctor_type, time_slot):
    with open(APPOINTMENTS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, problem, doctor_type, time_slot])

# Main workflow
speak("नमस्ते, मैं श्रीदेवी हूँ। आपकी सहायता कैसे कर सकती हूँ?")
user_input = listen()
print("User said:", user_input)

response = generate_response(user_input)
speak(response)

# Collect details and save appointment
name = "राहुल शर्मा"
problem = "पेट दर्द"
doctor_type = "गैस्ट्रोएंटेरोलॉजिस्ट"
time_slot = suggest_time_slots()[0]

save_appointment(name, problem, doctor_type, time_slot)
speak(f"आपका अपॉइंटमेंट {time_slot} के लिए बुक हो गया है। धन्यवाद!")