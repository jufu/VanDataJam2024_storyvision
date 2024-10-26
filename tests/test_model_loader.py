# Import the ModelLoader class from the modules folder
from modules.model_loader import ModelLoader


def test_generate_text():
    """
    Tests the ModelLoader's ability to load a model and generate text.
    """
    # Initialize ModelLoader with default model (Llama 2 7B)
    loader = ModelLoader()
    # Define a prompt to pass to the model
    prompt = "Once upon a time in a magical forest,"
    # Generate text based on the prompt
    output = loader.generate_text(prompt)
    # Print the generated text to verify the model's output
    print("Generated Text:", output)


# Run the test function if this script is executed directly
if __name__ == "__main__":
    test_generate_text()
