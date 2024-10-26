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

    def generate_audio(self, text, output_file="output.mp3"):
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
            tts = gTTS(text=text, lang=self.lang)
            # Save the audio to the specified file
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Error generating audio: {e}")
            return ""
