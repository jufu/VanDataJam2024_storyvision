from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from modules.ocr_processor import OCRProcessor
from modules.image_captioner import ImageCaptioner
from modules.description_enhancer import DescriptionEnhancer
from modules.text_to_speech import TextToSpeech
from modules.storytell import StoryTell
import os

app = FastAPI()

# Initialize modules with error handling
try:
    ocr_processor = OCRProcessor()
    image_captioner = ImageCaptioner()
    description_enhancer = DescriptionEnhancer()
    text_to_speech = TextToSpeech()
except Exception as e:
    print(f"Error initializing modules: {e}")
    ocr_processor, image_captioner, description_enhancer, text_to_speech = None, None, None, None


@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """
    Endpoint to process an uploaded image and return an audio file with a generated description.

    Args:
        file (UploadFile): Image file uploaded by the user.

    Returns:
        FileResponse: Path to the generated audio file.
    """
    # Check if all modules are available
    if not (ocr_processor and image_captioner and description_enhancer and text_to_speech):
        raise HTTPException(
            status_code=503, detail="Required modules are not available.")

    # Save the uploaded file
    image_path = f"./temp/{file.filename}"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    with open(image_path, "wb") as image_file:
        image_file.write(await file.read())

    # Step 1: Extract text from image (OCR)
    try:
        extracted_text = ocr_processor.extract_text(image_path)
    except Exception as e:
        print(f"Error during OCR: {e}")
        extracted_text = ""

    # Step 2: Generate image caption
    try:
        image_caption = image_captioner.generate_caption(image_path)
    except Exception as e:
        print(f"Error during image captioning: {e}")
        image_caption = "a scene from a storybook"

    # Combine OCR text and caption for description enhancement
    combined_text = f"{image_caption}. {extracted_text}"

    # Step 3: Enhance description
    try:
        enhanced_description = description_enhancer.enhance_description(
            combined_text)
    except Exception as e:
        print(f"Error during description enhancement: {e}")
        enhanced_description = "An engaging description could not be generated due to a processing error."

    # Step 4: OpenAI Storytell
    story_for_audio = None
    try:
        story_for_audio = StoryTell.storytell(enhanced_description)
    except Exception as e:
        print(f"Error during story enhancement: {e}")
        story_for_audio = "An engaging story could not be generated due to a processing error."

    # Step 5: Convert description to audio
    try:
        audio_path = "./temp/output.mp3"
        text_to_speech.generate_audio(story_for_audio, audio_path)
    except Exception as e:
        print(f"Error during text-to-speech generation: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate audio.")

    # Return the generated audio file
    return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")
