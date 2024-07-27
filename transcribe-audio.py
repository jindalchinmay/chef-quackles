import pyaudio
import wave
from openai import OpenAI
import threading
import time
import os

# Initialize the OpenAI client
client = OpenAI(api_key="sk-proj-Rumim2JuVmQwGGY8i2tAT3BlbkFJzL5s3JaOdTEn4GxbgyhR")

# Audio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Recording")

def record_audio():
    while True:
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        # Save the recorded data as a WAV file
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

def transcribe_audio():
    while True:
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            print(f"Transcription: {transcript.text}")
            os.remove(WAVE_OUTPUT_FILENAME)
        time.sleep(1)

# Start recording and transcription threads
recording_thread = threading.Thread(target=record_audio)
transcription_thread = threading.Thread(target=transcribe_audio)

recording_thread.start()
transcription_thread.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("* Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()