import pyaudio
import wave
from openai import OpenAI
import threading
import time
import os
import requests
import pymongo
import os 
from dotenv import load_dotenv
from voice import tts
load_dotenv()

print(os.getenv("OPENAI_API_KEY_REAL"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_REAL"))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()


client2 = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = client2["prompts"]
collection = db["prompts"]
print(collection)
collection.delete_many({})

def list_audio_devices():
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Input Device id {i} - {device_info.get('name')}")

def get_webcam_device_index():
    list_audio_devices()
    while True:
        try:
            device_index = 0 
            device_info = p.get_device_info_by_host_api_device_index(0, device_index)
            if device_info.get('maxInputChannels') > 0:
                return device_index
            else:
                print("Invalid input device. Please choose an input device.")
        except ValueError:
            print("Invalid input. Please enter a number.")

webcam_device_index = get_webcam_device_index()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=webcam_device_index,
                frames_per_buffer=CHUNK)

print("* Recording from selected device")

def record_audio():
    while True:
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


def transcribe_audio():
    prompt = ""
    index = 0
    state = False
    while True:
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    language="en" 
                )
            if ('chef' in transcript.text.lower() or 'hey' in transcript.text.lower()) and state == False:
                state = True
                index = 1
                prompt += transcript.text
            if state == True:
                if not index:
                    prompt += transcript.text
                index = 0
                if ('please' in transcript.text.lower()):
                    state = False
                    print(f"Transcription: {prompt}")
                    url = "http://172.20.10.12:8000/api/duck"
                    x = requests.post(url, json = {"prompt": prompt}, headers={"Content-Type": "application/json"})
                    data_voice = x.json().get("data")
                    print(data_voice)
                    tts(data_voice)
                    # tts(prompt)
                    prompt = ""
            print(f"Transcription: {prompt}")
            os.remove(WAVE_OUTPUT_FILENAME)
        time.sleep(0.1)

recording_thread = threading.Thread(target=record_audio)
transcription_thread = threading.Thread(target=transcribe_audio)

recording_thread.start()
transcription_thread.start()

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print("* Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()