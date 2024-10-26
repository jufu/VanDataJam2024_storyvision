from modules.text_to_speech import TextToSpeech


def test_generate_audio():
    """
    Tests the TextToSpeech class's ability to generate audio from text.
    """
    # Initialize TextToSpeech
    tts = TextToSpeech(lang="en")

    # Sample text to convert to audio
    text = "Once upon a time in a magical forest, a little kitten played happily."

    # Generate the audio file
    output_file = tts.generate_audio(text, "test_output.mp3")

    # Check if the audio file was created
    if output_file:
        print(f"Audio generated and saved to {output_file}")
    else:
        print("Failed to generate audio.")


# Run the test if this script is executed directly
if __name__ == "__main__":
    test_generate_audio()
