from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests


class LlamaStoryTeller:
    def __init__(self, model_name="gpt2-large", device=None):
        """
        Initializes the DescriptionEnhancer with a specified model.

        Args:
            model_name (str): Name of the text generation model to load.
            device (str): Device to use for model inference ('cuda' for GPU, 'cpu' for CPU).
                          Automatically detects GPU if available.
        """
        # Set device (default to GPU if available)
        # self.device = device if device else (
        #     "cuda" if torch.cuda.is_available() else "cpu")

        # Load the text generation model and tokenizer
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # self.model.to(self.device)
        self.api_url = "http://localhost:11434/api/generate"

    # def enhance_description(self, caption, max_length=100):
    #     """
    #     Enhances a caption to make it more engaging and narrative-driven.

    #     Args:
    #         caption (str): Initial caption to enhance.
    #         max_length (int): Maximum length of the generated description.

    #     Returns:
    #         str: Enhanced description with added detail and emotion.
    #     """
    #     # Updated prompt for storytelling with clear delimiters and simplified instruction
    #     prompt = f"Here is a caption from children's story book page: '{
    #         caption}'. Describe it vividly with excitement and emotions as if describing it to a blind child."

    #     # Tokenize the prompt and move it to the appropriate device
    #     inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

    #     # Generate the enhanced description with added parameters for creativity
    #     outputs = self.model.generate(
    #         inputs["input_ids"],
    #         max_new_tokens=max_length,
    #         pad_token_id=self.tokenizer.eos_token_id,
    #         attention_mask=inputs["attention_mask"],
    #         # temperature=0.8,  # Add randomness to avoid repetitive outputs
    #         # top_p=0.9         # Nucleus sampling to focus on top 90% probability
    #     )

    #     # Decode the output tokens to get the enhanced description
    #     enhanced_description = self.tokenizer.decode(
    #         outputs[0], skip_special_tokens=True)

    #     # Trim any part of the response that might repeat the prompt
    #     if prompt in enhanced_description:
    #         enhanced_description = enhanced_description.replace(
    #             prompt, "").strip()

    #     return enhanced_description

    def generate_story(self, text_from_visuals, extracted_text):
        """
        Sends a request to the Ollama API to enhance the caption into a
        child-friendly, engaging story.

        Args:
            caption (str): Initial caption to enhance.

        Returns:
            str: Enhanced description from the API response.
        """
        # Define the prompt for the API request
        # TODO Update with this prompt
        """"prompt": "Here is a caption from children's story book page: 'a cartoon of two girls talking to each other'. And here part of the story related to the image ' Once upon atime there lived twin sisters. Their names were Tinky and Pinky. Their mother told that they should not go to a particular pond. But they wanted to know what was there in the pond. So the went to the pond. suddenly friendly monster sprang up.'.Describe it vividly with excitement and emotions as if telling a story to visually impaired child. The story continues in next page so do not add anything that is not there in the prompt",
        """
        prompt = f"Imagine a magical scene based on this description for children: '{           text_from_visuals}'. Make it vivid, exciting, and full of emotions."

        # Set up the request payload
        payload = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }

        # Make the API request to Ollama
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses

            # Extract the text from the JSON response
            result = response.json()
            enhanced_description = result["response"]
            return enhanced_description.strip()

        except requests.RequestException as e:
            print(f"Error connecting to Ollama API: {e}")
            return "Error generating description."
