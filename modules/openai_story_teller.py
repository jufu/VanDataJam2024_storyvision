from openai import OpenAI
import os
import base64


class OpenAIStoryTeller:
    def __init__(self, lang="en"):
        """
        Initializes the TextToSpeech class for generating audio from text.

        Args:
            lang (str): Language code for TTS. Defaults to English ("en").
        """
        self.lang = lang

    def generate_story(self, image_path, extracted_text):
        """
        Generates a LLM optimized story from the provided text.

        Args:
            text (str): The text to convert
            output_file (str): The name of the output audio file.

        Returns:
            str: optimized story from chatgpt
        """
        try:
            # Set your OpenAI API key
            api_key = os.environ.get("OPENAI_API_KEY")

            client = OpenAI(
                api_key=api_key,  # this is also the default, it can be omitted
            )
            with open(image_path, "rb") as image_file:
                b64_image = base64.b64encode(image_file.read()).decode("utf-8")
                response = client.chat.completions.create(
                    messages=[
                        {
                        "role": "user",
                        "content": [
                            {
                            "type": "text",
                            "text": """You are a children's storybook author. You are given part of the story text and the picture from that page.
            Write a descriptive caption for the picture, so a small child who cannot see the image can understand what is happening.
            """,
                            },
                            {
                            "type": "text",
                            "text": extracted_text,
                            },
                            {
                            "type": "image_url",
                            "image_url": {
                                "url":  f"data:image/jpeg;base64,{b64_image}"
                            },
                            },
                        ],
                        }
                    ],
                    model="gpt-4o-mini",
                    temperature=0.3,  # Adjust the temperature to control the creativity of the response
                )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating llm optimized story: {e}")
            return ""
