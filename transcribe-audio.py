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
RECORD_SECONDS = 1.5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()


# TODO - clear database when this program is called

def list_audio_devices():
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:  # if it has input channels, it's an input device
            print(f"Input Device id {i} - {device_info.get('name')}")

def get_webcam_device_index():
    list_audio_devices()
    while True:
        try:
            device_index = 0  # You can change this back to user input if needed
            device_info = p.get_device_info_by_host_api_device_index(0, device_index)
            if device_info.get('maxInputChannels') > 0:
                return device_index
            else:
                print("Invalid input device. Please choose an input device.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Get the device index for the external webcam
webcam_device_index = get_webcam_device_index()

# Open stream with the selected device
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
        
        # Save the recorded data as a WAV file
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
                    language="en"  # Specify English language
                )
            if 'chef' in transcript.text.lower() and state == False:
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
                    # CALL API HERE with the current prompt string
                    prompt = ""
            print(f"Transcription: {prompt}")
            os.remove(WAVE_OUTPUT_FILENAME)
        time.sleep(0.1)

# Start recording and transcription threads
recording_thread = threading.Thread(target=record_audio)
transcription_thread = threading.Thread(target=transcribe_audio)

recording_thread.start()
transcription_thread.start()

try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print("* Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()