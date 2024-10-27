# Story Vision

This project provides an accessible, interactive storybook narrator for visually impaired children. By uploading images of storybook pages, users can generate engaging, emotion-filled audio descriptions, bringing stories to life in a fun and imaginative way.

## Table of Contents

1. [Features](#features)
2. [Project Architecture](#project-architecture)
3. [Setup and Installation](#setup-and-installation)
4. [Running the App](#running-the-app)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [Future Enhancements](#future-enhancements)

---

## Features

- **Image Upload**: Upload images of storybook pages.
- **OCR Processing**: Extracts any text present in the uploaded images.
- **Image Captioning**: Generates captions to provide context for the image.
- **Enhanced Description**: Transforms the caption into a vivid, child-friendly narrative.
- **Text-to-Speech (TTS)**: Converts the generated description into an audio file.
- **Interactive Web UI**: A user-friendly interface built with Streamlit for easy interaction.

---

## Project Architecture

The project consists of the following key components:

1. **Modules**:
   - `OCR Processor`: Extracts text from images.
   - `Image Captioner`: Generates captions for the image.
   - `Description Enhancer`: Converts the caption into an engaging narrative.
   - `Text-to-Speech (TTS)`: Converts text descriptions into audio files.
2. **API**:
   - FastAPI endpoints handle image processing and return the generated audio.
3. **UI**:
   - Streamlit app allows users to interact with the system via a web interface.

---

## Setup and Installation

### 1. Prerequisites

- **Python 3.12.2**
- **Git**
- **[Ollama](https://ollama.com/)** (for running Llama 2, if available)
- **Tesseract OCR** (for text extraction from images)

### 2. Clone the Repository

```bash
git clone https://github.com/jufu/VanDataJam2024_storyvision
cd VanDataJam2024_storyvision
```

### 3. Set Up the Virtual Environment

Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 4. Install Dependencies

Install project dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Install and Set Up Tesseract OCR

- **macOS**: `brew install tesseract`
- **Ubuntu**: `sudo apt update && sudo apt install tesseract-ocr`
- **Windows**: Download the installer from [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and follow the installation instructions.

### 6. Install and Set Up Ollama (for Llama 2)

To use Llama 2 for description enhancement, install **Ollama**:

1. **Install Ollama**:
   - **macOS**: `brew install ollama/tap/ollama`
   - For other platforms, visit the [Ollama website](https://ollama.com/).

2. **Pull the Llama 2 Model**:
   ```bash
   ollama pull llama2
   ```

3. **Start the Ollama API**:
   ```bash
   ollama serve
   ```

   This starts the Ollama API at `http://localhost:11434`, which the app will use for generating descriptions.

### 7. Environment Setup

This project requires some environment variables (like API keys or other sensitive information) to be configured locally. To simplify setup, we’ve included a `.env_template` file that you can use as a reference for creating your own `.env` file.

#### **Steps to Set Up Your Local Environment Variables**

1. **Copy the Template File**:
   - In the project’s root directory, copy the `.env_template` file to create your own `.env` file:

     ```bash
     cp .env_template .env
     ```

2. **Edit the `.env` File**:
   - Open the newly created `.env` file and update each environment variable with your local or project-specific values.

   - For example, if the `.env_template` contains:
     ```plaintext
     MY_API_KEY=your_api_key_here
     ANOTHER_API_KEY=another_api_key_here
     TTS_SERVICE=gtts
     ```
   - Replace `your_api_key_here` and other placeholders with your actual values:
     ```plaintext
     MY_API_KEY=abcdef12345
     ANOTHER_API_KEY=zyx98765
     TTS_SERVICE=gtts
     ```

3. **Save the `.env` File**:
   - After updating the variables, save the `.env` file. These values will now load automatically whenever the app runs.

#### **Using Environment Variables in the Code**

- Environment variables set in `.env` will automatically be accessible in the application, ensuring that sensitive information like API keys is never hardcoded into the source code.
  
- For team members, please don’t commit your `.env` file to version control to keep sensitive information secure. The `.env_template` file is included in version control for reference only.

#### **Example Variables in `.env_template`**

Here’s an example of what the `.env_template` file might contain:

```plaintext
# API Keys
MY_API_KEY=your_api_key_here
ANOTHER_API_KEY=another_api_key_here

# TTS Service (default: gtts)
TTS_SERVICE=gtts
```

Each team member should replace the placeholders with their own credentials and preferred settings.

---

### **Note on Security**

The `.env` file is included in `.gitignore` to ensure it is not accidentally committed to version control. Always double-check before committing that sensitive information is not being pushed to the repository.
---
## Running the App

The app includes two main components: the FastAPI backend and the Streamlit frontend. Make sure Ollama’s API server is running if you plan to use Llama 2.

### Start the FastAPI Server

In one terminal window, start the FastAPI server:

```bash
uvicorn api.main:app --reload
```

- This starts the FastAPI frontend at `http://127.0.0.1:8000`.
- You can test the API endpoints via the documentation at `http://127.0.0.1:8000/docs`.

### App Screenshots

---

## Usage

1. **Open the Streamlit UI**: Go to `http://localhost:8501`.
2. **Upload an Image**: Use the file uploader to select an image containing a storybook page.
3. **Generate Audio**: Click "Generate Audio Description" to process the image.
4. **Play the Audio**: Once processing is complete, listen to the generated audio description.

---

## Troubleshooting

### Common Issues

- **Error: `address already in use`**: Ensure there’s only one instance of Ollama or FastAPI running on the same port.
- **404 Error on API Requests**: Verify that Ollama is running on `http://localhost:11434`. Restart if necessary.
- **Model Initialization Failure**: If a module fails to initialize, the app will continue but may return a message saying, “Service is currently unavailable.”
- **Tesseract Not Found**: Ensure Tesseract is installed correctly and available in your system PATH.

---
