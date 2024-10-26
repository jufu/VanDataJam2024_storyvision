import streamlit as st
import requests
from io import BytesIO

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/process-image"

st.title("Accessible Storybook Narrator")
st.write("Upload an image, and the app will generate an engaging audio description!")

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose an image file", type=["jpg", "jpeg", "png"])

# Display button to trigger processing
if uploaded_file is not None:
    if st.button("Generate Audio Description"):
        # Send the uploaded file to the FastAPI endpoint
        files = {"file": (uploaded_file.name, uploaded_file,
                          "multipart/form-data")}
        response = requests.post(FASTAPI_URL, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            # Load the audio content
            audio_data = BytesIO(response.content)
            # Play the audio in Streamlit
            st.audio(audio_data, format="audio/mp3")
            st.success("Audio description generated successfully!")
        else:
            st.error("Failed to generate audio. Please try again.")
