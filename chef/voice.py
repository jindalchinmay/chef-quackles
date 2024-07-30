import os
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import pygame
import warnings
from dotenv import load_dotenv
warnings.filterwarnings("ignore", category=UserWarning)

def tts(text):
    load_dotenv()

    api_key = os.getenv("ELEVENLABS_API_KEY")

    client = ElevenLabs(api_key=api_key)


    def text_to_speech_stream(text: str) -> IO[bytes]:
        try:
            response = client.text_to_speech.convert(
                voice_id="jBpfuIE2acCO8z3wKNLl",  
                optimize_streaming_latency=3, 
                output_format="mp3_44100_128", 
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.6,  
                    similarity_boost=0.7, 
                    style=0.0,
                    use_speaker_boost=True,
                    speed=2.5, 
                ),
            )

            audio_stream = BytesIO()
            for chunk in response:
                if chunk:
                    audio_stream.write(chunk)
            audio_stream.seek(0)
            return audio_stream
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    pygame.mixer.init(frequency=44100)


    audio_stream = text_to_speech_stream(text)

    if audio_stream:
        output_file = "output.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_stream.getvalue())
        print(f"Audio saved to {output_file}")
        
        try:
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(60)  
            
            print("Audio playback completed")
        except Exception as e:
            print(f"Failed to play audio: {str(e)}")
    else:
        print("Failed to generate audio")

    pygame.mixer.quit()


if __name__ == "__main__":
    tts("This is a test of the much faster speech at 2.5x speed. Is it clear and understandable?")