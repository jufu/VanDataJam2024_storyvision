import os
from modules.image_captioner import ImageCaptioner


def test_generate_caption():
    """
    Tests the ImageCaptioner's ability to generate captions for an image.
    """
    # Initialize the ImageCaptioner
    captioner = ImageCaptioner()

    # Define image path dynamically (make sure the image is in the specified folder)
    image_folder = './tests/'
    image_name = 'childrens_book_page.png'  # Replace with your test image file
    image_path = os.path.join(image_folder, image_name)

    # Generate the caption for the image
    caption = captioner.generate_caption(image_path)

    # Print the generated caption
    print("Generated Caption:", caption)


# Run the test if this script is executed directly
if __name__ == "__main__":
    test_generate_caption()
