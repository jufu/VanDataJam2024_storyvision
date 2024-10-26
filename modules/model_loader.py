# Import necessary libraries from the Hugging Face Transformers and PyTorch
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# llama model name meta-llama/Llama-2-7b-hf
# gpt2 model name gpt2
# gpt2 large model name gpt2-large


class ModelLoader:
    def __init__(self, model_name="gpt2-large", device=None):
        """
        Initializes the ModelLoader class, which handles loading and inference 
        for different language models. It defaults to the Llama 2 7B model.

        Args:
            model_name (str): Name of the model to load. Defaults to Llama 2 7B.
            device (str): Device to use for model inference ('cuda' for GPU, 'cpu' for CPU).
                          Automatically detects GPU if available.
        """
        # Determine device type (GPU if available, else CPU)
        self.device = device if device else (
            "cuda" if torch.cuda.is_available() else "cpu")
        # Save the initial model name
        self.model_name = model_name
        # Load the model and tokenizer
        self.model, self.tokenizer = self.load_model()

    def load_model(self):
        """
        Loads the model and tokenizer for the specified model name and moves the model 
        to the appropriate device.

        Returns:
            model (torch.nn.Module): Loaded model.
            tokenizer (transformers.PreTrainedTokenizer): Tokenizer for the model.
        """
        print(f"Loading model: {self.model_name}")
        # Load the tokenizer for text processing
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        # Load the model with automatic device mapping for GPU/CPU
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name, device_map="auto")
        # Move the model to the specified device
        model.to(self.device)
        return model, tokenizer

    def generate_text(self, prompt, max_length=100):
        """
        Generates text based on a given prompt using the loaded model.

        Args:
            prompt (str): Input text prompt for the model to generate a response.
            max_length (int): Maximum length of generated text.

        Returns:
            str: Generated text output from the model.
        """
        # Tokenize the input prompt and move it to the appropriate device
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Add pad_token_id to prevent warnings for models without padding token
        pad_token_id = self.tokenizer.eos_token_id if self.tokenizer.pad_token_id is None else self.tokenizer.pad_token_id

        # Generate output from the model with the specified max length and attention mask
        outputs = self.model.generate(
            inputs["input_ids"],
            max_new_tokens=max_length,
            attention_mask=inputs["attention_mask"],
            pad_token_id=pad_token_id  # Setting pad_token_id to avoid warnings
        )

        # Decode the output tokens to readable text
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text

    def set_model(self, model_name):
        """
        Allows switching to a different model by updating the model_name and 
        reloading the model and tokenizer.

        Args:
            model_name (str): Name of the new model to load.
        """
        # Update model name and reload model and tokenizer
        self.model_name = model_name
        self.model, self.tokenizer = self.load_model()
