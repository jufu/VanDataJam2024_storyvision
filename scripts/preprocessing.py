import pymupdf
import io
from PIL import Image
import re


def extract_tex(doc, output_txt):
    # create output file
    out = open(output_txt, 'wb')

    # iterate through pages and extract text
    for page in doc:
        text = page.get_text()
        clean_text = re.sub(r'\s+', ' ', text)
        out.write(clean_text.encode('utf-8'))
        out.write('\n'.encode('utf-8'))
    out.close()


def extract_images(doc):
    for page in doc:
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))
            image.save(f"data/processed/page_{page.number}_image_{img_index}.png")


def preprocess_story(pdf_path, output_txt):
    doc = pymupdf.open(pdf_path)
    extract_tex(doc, output_txt)
    extract_images(doc)
    doc.close()


# running with example story
pdf_file = 'data/60810-the-picnic.pdf'
output_txt = 'data/processed/text.txt'
preprocess_story(pdf_file, output_txt)
