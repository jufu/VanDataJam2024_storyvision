from openai import OpenAI
import os


class OpenAIStoryTeller:
    def __init__(self, lang="en"):
        """
        Initializes the TextToSpeech class for generating audio from text.

        Args:
            lang (str): Language code for TTS. Defaults to English ("en").
        """
        self.lang = lang

    def generate_story(self, text_from_visuals, extracted_text):
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

            response = client.chat.completions.with_raw_response.create(
                messages=[
                    {
                        "role": "system",
                        "content": """Imagine you are telling a story from one page of a children’s storybook page. Summarize the description in simple, engaging language as if you are narrating a story aloud, using phrases and words that bring each scene to life and create a warm, friendly tone. Avoid adding any new information that is not in the text of the page. Keep it under 50 words
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"Here is the page description of the visuals: {text_from_visuals}. More importantly, here is a text from the page in the page: {extracted_text}.",
                    },
                ],
                model="gpt-4o-mini",
                temperature=0.3,  # Adjust the temperature to control the creativity of the response
            )
            print(response.headers.get("x-ratelimit-limit-tokens"))

            # get the object that `chat.completions.create()` would have returned
            completion = response.parse()
            first_choice = completion.choices[0].message.content

            return first_choice
        except Exception as e:
            print(f"Error generating llm optimized story: {e}")
            return ""
