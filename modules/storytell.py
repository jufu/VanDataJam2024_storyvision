from openai import OpenAI
import os


class StoryTell:
    def __init__(self, lang="en"):
        """
        Initializes the TextToSpeech class for generating audio from text.

        Args:
            lang (str): Language code for TTS. Defaults to English ("en").
        """
        self.lang = lang

    def generate_storytell(self, text):
        """
        Generates an audio file from the provided text.

        Args:
            text (str): The text to convert to speech.
            output_file (str): The name of the output audio file.

        Returns:
            str: Path to the generated audio file.
        """
        try:
            # Set your OpenAI API key
            api_key = "sk-YqhOmfvWOi_8YrEX0UcDa3IPlVzF1IAqnlmQ-1VfehT3BlbkFJlm_TVhZq1G4JG13QCItAWg96Bt1KC1ynG3NVugio4A"

            client = OpenAI(
                api_key=api_key,  # this is also the default, it can be omitted
            )

            response = client.chat.completions.with_raw_response.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Imagine you are telling a story to a young child based on a children’s storybook page description. Summarize the description in simple, engaging language as if you are narrating a story aloud, using phrases and words that bring each scene to life and create a warm, friendly tone. Keep it concise but add a sense of wonder or excitement that will work well for text-to-speech narration.",
                    },
                    {
                        "role": "user",
                        "content": f"Here is the page description: {text}",
                    },
                ],
                model="gpt-4o-mini",
            )
            print(response.headers.get("x-ratelimit-limit-tokens"))

            # get the object that `chat.completions.create()` would have returned
            completion = response.parse()
            first_choice = completion.choices[0].message.content

            return first_choice
        except Exception as e:
            print(f"Error generating llm optimized story: {e}")
            return ""
