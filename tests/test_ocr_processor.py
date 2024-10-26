from modules.ocr_processor import OCRProcessor


def test_ocr_extraction():
    """
    Tests the OCRProcessor's ability to extract text from an image.
    """
    # Initialize OCRProcessor (using English language)
    ocr = OCRProcessor(lang="eng")
    # Test with an example image (replace 'sample_image.png' with your image path)
    image_path = './tests/childrens_book_page.png'
    extracted_text = ocr.extract_text(image_path)
    # Print the extracted text for verification
    print("Extracted Text:", extracted_text)


# Run the test if this script is executed directly
if __name__ == "__main__":
    test_ocr_extraction()
