from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from modules.ocr_processor import OCRProcessor
from modules.image_captioner import ImageCaptioner
from modules.text_to_speech import TextToSpeech
from modules.openai_story_teller import OpenAIStoryTeller
from modules.llama_story_teller import LlamaStoryTeller
from modules.story_teller import StoryTeller
from modules.pdf_extractor import PDFExtractor
import os
import uvicorn
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# Initialize modules with error handling
try:
    ocr_processor = OCRProcessor()
    image_captioner = ImageCaptioner()
    llama_story_teller = LlamaStoryTeller()
    text_to_speech = TextToSpeech()
    OpenAIStoryTeller = OpenAIStoryTeller()
except Exception as e:
    print(f"Error initializing modules: {e}")
    ocr_processor, image_captioner, llama_story_teller, text_to_speech = None, None, None, None


@app.post("/process-image")
async def process_image(file: UploadFile = File(...), tts_option: str = Form("Google TTS"), llm_option: str = Form("llama2")):
    """
    Endpoint to process an uploaded image and return an audio file with a generated description.

    Args:
        file (UploadFile): Image file uploaded by the user.

    Returns:
        FileResponse: Path to the generated audio file.
    """
    # Check if all modules are available
    if not (ocr_processor and image_captioner and llama_story_teller and text_to_speech):
        raise HTTPException(
            status_code=503, detail="Required modules are not available.")

    # Save the uploaded file
    output_folder = "./temp"
    books_folder = f"{output_folder}/books"
    pdf_path = f"{books_folder}/{file.filename}"
    text_folder = f"{output_folder}/text"
    images_folder = f"{output_folder}/images"
    audio_folder = f"{output_folder}/audio"

    # Create each folder directly
    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(await file.read())

    # # Step 1: Extract text from image (OCR)
    # try:
    #     extracted_text = ocr_processor.extract_text(image_path)
    # except Exception as e:
    #     print(f"Error during OCR: {e}")
    #     extracted_text = ""

    # Step 1: Preprocess PDF
    try:
        pdf_extractor = PDFExtractor(pdf_path, output_folder)
        extracted_pdf = pdf_extractor.preprocess_story()
        uuid = extracted_pdf["unique_id"]
        text_files = extracted_pdf["text_files"]
        images = extracted_pdf["image_files"]
    except Exception as e:
        print(f"Error during PDF extraction: {e}")
        extracted_text = ""

    # default to first image
    image_path = images[0]
    extracted_text = text_files[0]

    # Step 2: Generate image caption
    try:
        image_caption = image_captioner.generate_caption(image_path)
    except Exception as e:
        print(f"Error during image captioning: {e}")
        image_caption = "a scene from a storybook"

    # Step 3: Generate Story
    try:
        story_teller = StoryTeller(llm_option)
        story_for_audio = story_teller.generate_story(
            text_from_visuals=image_caption, extracted_text=extracted_text)
    except Exception as e:
        print(f"Error during description enhancement: {e}")
        story_for_audio = "An engaging description could not be generated due to a processing error."

    # Step 4: Convert description to audio
    try:
        audio_file_name = f"{uuid}_page_0_audio_0.mp3"
        audio_file_path = f"{audio_folder}/{audio_file_name}"
        text_to_speech.generate_audio(
            story_for_audio, audio_file_path, tts_option)
    except Exception as e:
        print(f"Error during text-to-speech generation: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate audio.")

    # Return the generated audio file
    return FileResponse(audio_file_path, media_type="audio/mpeg", filename=audio_file_name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
