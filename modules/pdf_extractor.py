import pymupdf  #
import io
import os
import re
from PIL import Image
import uuid


class PDFExtractor:
    def __init__(self, pdf_path, output_folder):
        """
        Initializes the PDFExtractor with the PDF path and output folder.

        Args:
            pdf_path (str): Path to the PDF file.
            output_folder (str): Folder to save the extracted text and images.
        """
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.unique_id = self._generate_unique_id()
        self.text_output_folder = os.path.join(output_folder, "text")
        self.image_output_folder = os.path.join(output_folder, "images")

        # Ensure output directories exist
        os.makedirs(self.text_output_folder, exist_ok=True)
        os.makedirs(self.image_output_folder, exist_ok=True)

    def _generate_unique_id(self):
        """
        Generates a unique identifier for each PDF processing session.

        Returns:
            str: A unique identifier string.
        """
        return str(uuid.uuid4())

    def _extract_text(self, doc):
        """
        Extracts text from each page in the PDF document and saves it to separate text files.

        Args:
            doc (pymupdf.Document): The PDF document.

        Returns:
            list: List of paths to the saved text files.
            list: List of page numbers to extract images from.
        """
        text_paths = []
        texts = []
        pages = []
        for i, page in enumerate(doc):
            text = page.get_text()
            clean_text = re.sub(r'\s+', ' ', text)
            if re.search(r'\d+/\d+\s*$', clean_text):
                clean_text = re.sub(r' \d+/\d+\s*$', '', clean_text)
                text_path = os.path.join(self.text_output_folder, f"{
                                        self.unique_id}_page_{i}.txt")
                with open(text_path, 'wb') as out:
                    out.write(clean_text.encode('utf-8'))
                text_paths.append(text_path)
                texts.append(clean_text)
                pages.append(i)

        return text_paths, pages, texts

    def _extract_images(self, doc, pages):
        """
        Extracts images from each page in the PDF document and saves them as PNG files.

        Args:
            doc (pymupdf.Document): The PDF document.
            pages (list): List of page numbers to extract images from.

        Returns:
            list: List of paths to the saved images.
        """
        images_paths = []
        for page in doc:
            if page.number in pages:
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image_path = os.path.join(self.image_output_folder, f"{self.unique_id}_page_{page.number}_image..png")
                    image.save(image_path)
                    images_paths.append(image_path)
        return images_paths

    def preprocess_story(self):
        """
        Processes the PDF file to extract text and images with unique identifiers.

        Returns:
            dict: Dictionary containing lists of paths to the saved text and image files.
        """
        doc = pymupdf.open(self.pdf_path)

        # Extract text and images
        text_paths, pages, texts = self._extract_text(doc)
        images_paths = self._extract_images(doc, pages)

        doc.close()

        # Return a dictionary with paths to the text and image files
        return {
            "unique_id": self.unique_id,
            "text_files": text_paths,
            "texts": texts,
            "image_files": images_paths
        }
