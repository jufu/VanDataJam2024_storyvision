from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


class ImageCaptioner:
    def __init__(self, model_name="Salesforce/blip-image-captioning-base", device=None):
        """
        Initializes the ImageCaptioner with a specified model.

        Args:
            model_name (str): Name of the image captioning model to load.
            device (str): Device to use for model inference ('cuda' for GPU, 'cpu' for CPU).
                          Automatically detects GPU if available.
        """
        # Set device (default to GPU if available)
        self.device = device if device else (
            "cuda" if torch.cuda.is_available() else "cpu")

        # Load the image captioning model and processor
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)

    def generate_caption(self, image_path):
        """
        Generates a caption for a given image.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: Generated caption describing the content of the image.
        """
        try:
            # Open the image
            image = Image.open(image_path)

            # Preprocess the image and move it to the appropriate device
            inputs = self.processor(
                images=image, return_tensors="pt").to(self.device)

            # Generate the caption
            outputs = self.model.generate(**inputs)

            # Decode the output tokens to get the caption
            caption = self.processor.decode(
                outputs[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            print(f"Error generating caption for image {image_path}: {e}")
            return ""
