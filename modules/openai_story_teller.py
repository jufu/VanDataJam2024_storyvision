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


    def generate_openai_caption(self, image_path, extracted_text):
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
            print("Page text: " , extracted_text)
            with open(image_path, "rb") as image_file:
                b64_image = base64.b64encode(image_file.read()).decode("utf-8")
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": ["""
                                You are an enthusiastic, friendly storyteller assisting a parent reading to a young child with visual impairments.
                                For each message, you will receive the text and an image from the page in a book.

                                Respond with the text from the page first, and try to understand the people and objects in the image and describe them in more detail at the end of the text.
                                If there are names or objects in the text, try to identify it in the image.

                                Aim for 2-3 sentences that are warm, vivid, and suited for a young child's attention span.
                            """]
                            #Use the story's language, themes, and tone to describe the image in a fun, simple, and engaging way.
                            #Focus on bringing the picture to life with expressive descriptions that capture emotions, colors, and any action happening, so the child can imagine the story fully.
                        },
                        {
                        "role": "user",
                        "content": [
                            # {
                            # "type": "text",
                            # "text": """You are a parent reading a story book to your child who has impaired vision. You are given the text of the story and the picture from that page.
                            #             Use the story text to help understand what is happening in the picture and write a descriptive caption for the picture.
                            #             Use fun and expressive language so a small child who cannot see the image can understand what is happening. Keep the caption to 2-3 sentences.
                            #         """,
                            # },
                            {
                            "type": "text",
                            "text": "Text from the page:" + extracted_text,
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
                    temperature=0.2,  # Adjust the temperature to control the creativity of the response
                )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating llm optimized story: {e}")
            return ""
