from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from modules.ocr_processor import OCRProcessor
from modules.image_captioner import ImageCaptioner
from modules.description_enhancer import DescriptionEnhancer
from modules.text_to_speech import TextToSpeech
import os

app = FastAPI()

# Initialize modules
ocr_processor = OCRProcessor()
image_captioner = ImageCaptioner()
description_enhancer = DescriptionEnhancer()
text_to_speech = TextToSpeech()


@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """
    Endpoint to process an uploaded image and return an audio file with a generated description.

    Args:
        file (UploadFile): Image file uploaded by the user.

    Returns:
        FileResponse: Path to the generated audio file.
    """
    # Save the uploaded file
    image_path = f"./temp/{file.filename}"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    with open(image_path, "wb") as image_file:
        image_file.write(await file.read())

    # Step 1: Extract text from image (OCR)
    extracted_text = ocr_processor.extract_text(image_path)

    # Step 2: Generate image caption
    image_caption = image_captioner.generate_caption(image_path)

    # Combine OCR text and caption for description enhancement
    combined_text = f"{image_caption}. {extracted_text}"

    # Step 3: Enhance description
    enhanced_description = description_enhancer.enhance_description(
        combined_text)

    # Step 4: Convert description to audio
    audio_path = "./temp/output.mp3"
    text_to_speech.generate_audio(enhanced_description, audio_path)

    # Return the generated audio file
    return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")
