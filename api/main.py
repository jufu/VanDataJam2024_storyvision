from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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

# initialize templates
app.mount("/static", StaticFiles(directory="public/static"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")
templates = Jinja2Templates(directory="public")

# initialize folders
output_folder = "./temp"
books_folder = f"{output_folder}/books"
text_folder = f"{output_folder}/text"
images_folder = f"{output_folder}/images"
audio_folder = f"{output_folder}/audio"

# Create each folder directly
os.makedirs(books_folder, exist_ok=True)
os.makedirs(images_folder, exist_ok=True)
os.makedirs(audio_folder, exist_ok=True)
os.makedirs(text_folder, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Endpoint to render the homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})


async def generate_image_caption(image_path):
    """
    Function to generate a caption for an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Generated caption for the image.
    """
    print(f"Generating caption for image: {image_path}")
    try:
        image_caption = image_captioner.generate_caption(image_path)
    except Exception as e:
        print(f"Error during image captioning: {e}")
        image_caption = "a scene from a storybook"
    return image_caption


async def generate_story_from_image_and_text_openai(image_path, extracted_text):
    """
    Function to generate a story from text.

    Args:
        text (str): Text to generate a story from.

    Returns:
        str: Generated story.
    """
    print(f"Generating story from text")
    try:

        story_for_audio = OpenAIStoryTeller.generate_openai_caption(
            image_path, extracted_text)
    except Exception as e:
        print(f"Error during description enhancement: {e}")
        story_for_audio = "An engaging description could not be generated due to a processing error."
    return story_for_audio


async def generate_story_from_text(image_caption, extracted_text, llm_option):
    """
    Function to generate a story from text.

    Args:
        text (str): Text to generate a story from.

    Returns:
        str: Generated story.
    """
    print(f"Generating story from text")
    try:
        story_teller = StoryTeller(llm_option)
        story_for_audio = story_teller.generate_story(
            text_from_visuals=image_caption, extracted_text=extracted_text)
    except Exception as e:
        print(f"Error during description enhancement: {e}")
        story_for_audio = "An engaging description could not be generated due to a processing error."
    return story_for_audio


async def generate_audio_from_text(uuid, index, tts_option, story_for_audio):
    print(f"Generating audio for story, uuid: {uuid}, index: {index}")
    try:
        audio_file_name = f"{uuid}_page_{index}_audio.mp3"
        audio_file_path = f"{audio_folder}/{audio_file_name}"
        text_to_speech.generate_audio(
            story_for_audio, audio_file_path, tts_option)
    except Exception as e:
        print(f"Error during text-to-speech generation: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate audio.")
    return audio_file_path


@app.post("/process-image")
async def process_image(file: UploadFile = File(...), tts_option: str = Form("ElevenLabs TTS"), llm_option: str = Form("llama2")):
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
    pdf_path = f"{books_folder}/{file.filename}"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(await file.read())

    # Step 1: Preprocess PDF
    try:
        pdf_extractor = PDFExtractor(pdf_path, output_folder)
        extracted_data = pdf_extractor.preprocess_story()
        uuid = extracted_data["unique_id"]
        text_files = extracted_data["text_files"]
        images = extracted_data["image_files"]
    except Exception as e:
        print(f"Error during PDF extraction: {e}")
        extracted_text = ""

    # TODO for now we are generating all audio files at once. We can change this to generate audio files one by one to optimize the process
    audio_files = []
    for i in range(len(images)):
        image_path = images[i]
        extracted_text = ""
        with open(text_files[i], "r") as text_file:
            extracted_text = text_file.read()

        # # Step 2: Generate image caption
        # image_caption = await generate_image_caption(image_path)

        # # Step 3: Generate Story
        # story_for_audio = await generate_story_from_text(image_caption=image_caption,
        #                                                  extracted_text=extracted_text,
        #                                                  llm_option=llm_option)

        # Replace above two steps with OpenAI story generation
        story_for_audio = await generate_story_from_image_and_text_openai(image_path, extracted_text)

        # Step 4: Convert description to audio
        audio_file_path = await generate_audio_from_text(uuid, i, tts_option, story_for_audio)

        audio_files.append(audio_file_path)

    # Return the generated audio file
    extracted_data["audio_files"] = audio_files
    print(f"Returning extracted data: {extracted_data}")
    # return FileResponse(audio_file_path, media_type="audio/mpeg", filename=audio_file_name)
    return JSONResponse(content=extracted_data)


@app.post("/generate_audio")
async def generate_audio(uuid: str = Form(...),
                         index: int = Form(...), tts_option: str = Form("Google TTS"), llm_option: str = Form("llama2")):
    print(f"Generating audio for uuid: {uuid}, index: {index}")
    # Step 1 : create image path and text path from uuid and index
    image_path = f"{images_folder}/{uuid}_page_{index}_image.png"
    text_path = f"{text_folder}/{uuid}_page_{index}.txt"

    # Step 2: Read text from text file
    with open(text_path, "r") as text_file:
        extracted_text = text_file.read()

    # # Step 3: Generate image caption
    # image_caption = await generate_image_caption(image_path)

    # # Step 4: Generate Story
    # story_for_audio = await generate_story_from_text(image_caption=image_caption,
    #                                                  extracted_text=extracted_text,
    #                                                  llm_option=llm_option)

    # Replace above two steps with OpenAI story generation
    story_for_audio = await generate_story_from_image_and_text_openai(image_path, extracted_text)

    # Step 5: Convert description to audio
    audio_file_path = await generate_audio_from_text(uuid, index, tts_option, story_for_audio)
    data = {"audio_files": [audio_file_path]}
    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
