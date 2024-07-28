import os
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import pygame
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def tts(text):
    client = ElevenLabs(api_key="sk_48bfa043107801a1bdc4d352826f33892ef406b38420ab10")


    def text_to_speech_stream(text: str) -> IO[bytes]:
        try:
            response = client.text_to_speech.convert(
                voice_id="jBpfuIE2acCO8z3wKNLl",  # fin pre-made voice
                optimize_streaming_latency=3,  # Increased for even faster speech
                output_format="mp3_44100_128",  # Higher quality audio
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.6,  # Slightly increased for more consistent output at high speed
                    similarity_boost=0.7,  # Further reduced to allow for much faster speech
                    style=0.0,
                    use_speaker_boost=True,
                    speed=2.5,  # Increased to 2.5x speed as requested
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

    # Initialize pygame mixer
    pygame.mixer.init(frequency=44100)  # Match the audio output format

    # Example usage
    audio_stream = text_to_speech_stream(text)

    if audio_stream:
        # Save the audio file
        output_file = "output.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_stream.getvalue())
        print(f"Audio saved to {output_file}")
        
        # Play the audio file
        try:
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(60)  # Increased to 60 for smoother playback at high speed
            
            print("Audio playback completed")
        except Exception as e:
            print(f"Failed to play audio: {str(e)}")
    else:
        print("Failed to generate audio")

    # Quit pygame mixer
    pygame.mixer.quit()

#Example usage
# if __name__ == "__main__":
#     tts("This is a test of the much faster speech at 2.5x speed. Is it clear and understandable?")