from dotenv import load_dotenv
from elevenlabs import Voice, VoiceSettings, play, save
from elevenlabs.client import ElevenLabs
from gtts import gTTS
import os


class TextToSpeech:
    def __init__(self, lang="en"):
        """
        Initializes the TextToSpeech class for generating audio from text.

        Args:
            lang (str): Language code for TTS. Defaults to English ("en").
        """
        self.lang = lang
        self.elevellabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    def generate_audio(self, text, output_file="output.mp3", tts_option="ElevenLabs TTS"):
        """
        Generates an audio file from the provided text.

        Args:
            text (str): The text to convert to speech.
            output_file (str): The name of the output audio file.

        Returns:
            str: Path to the generated audio file.
        """
        try:
            # Initialize gTTS with the text and specified language
            if tts_option == "Google TTS":
                tts = gTTS(text=text, lang=self.lang)
                # Save the audio to the specified file
                tts.save(output_file)
                return output_file
            # Elevenlabs TTS
            elif tts_option == "ElevenLabs TTS":
                print("Generating audio using ElevenLabs TTS")
                # initialize eleven labs client
                client = ElevenLabs(
                    api_key=self.elevellabs_api_key
                )
                audio = client.generate(
                    text=text,
                    voice=Voice(
                        voice_id='XB0fDUnXU5powFXDhCwa',
                        # expected to be greater or equal to 0.0 and less or equal to 1.0
                        settings=VoiceSettings(
                            stability=0, similarity_boost=1, style=1, use_speaker_boost=True)
                    )
                )
                # save audiot to output_file
                save(audio, output_file)
        except Exception as e:
            print(f"Error generating audio: {e}")
            return ""
