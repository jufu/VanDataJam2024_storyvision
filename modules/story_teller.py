from modules.openai_story_teller import OpenAIStoryTeller
from modules.llama_story_teller import LlamaStoryTeller


class StoryTeller:
    def __init__(self, lang="en", llm_option="llama2"):
        """
        Initializes the StoryTeller class for generating stories from text.

        Args:
            lang (str): Language code for storytelling. Defaults to English ("en").
        """
        self.lang = lang
        self.llm_option = llm_option

    def _generate_llama_story(self, text_from_visuals, extracted_text):
        """
        Generates a story using the Llama model.

        Args:
            text_from_visuals (str): The text from the image caption.
            extracted_text (str): The extracted text from the image.

        Returns:
            str: The generated story.
        """
        llama_story_teller = LlamaStoryTeller()
        return llama_story_teller.generate_story(text_from_visuals, extracted_text)

    def _generate_openai_story(self, text_from_visuals, extracted_text):
        """
        Generates a story using the OpenAI model.

        Args:
            text_from_visuals (str): The text from the image caption.
            extracted_text (str): The extracted text from the image.

        Returns:
            str: The generated story.
        """
        openai_story_teller = OpenAIStoryTeller()
        return openai_story_teller.generate_story(text_from_visuals, extracted_text)

    def generate_story(self, text_from_visuals, extracted_text):
        """
        Generates a story from the provided text.

        Args:
            text_from_visuals (str): The text from the image caption.
            extracted_text (str): The extracted text from the image.
            llm_option (str): The LLM model to use for story generation.

        Returns:
            str: The generated story.
        """
        if self.llm_option == "llama2":
            return self._generate_llama_story(text_from_visuals, extracted_text)
        elif self.llm_option == "openai":
            return self._generate_openai_story(text_from_visuals, extracted_text)
        else:
            # TODO add default option
            return ""
