from PIL import Image
import pytesseract


class OCRProcessor:
    def __init__(self, lang="eng"):
        """
        Initializes the OCRProcessor for extracting text from images.

        Args:
            lang (str): Language code for OCR. Defaults to English ("eng").
        """
        self.lang = lang

    def extract_text(self, image_path):
        """
        Extracts text from an image file using Tesseract OCR.

        Args:
            image_path (str): Path to the image file to process.

        Returns:
            str: Extracted text from the image.
        """
        try:
            # Open the image file
            image = Image.open(image_path)
            # Use Tesseract to extract text from the image
            text = pytesseract.image_to_string(image, lang=self.lang)
            return text.strip()
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return ""
