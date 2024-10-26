import streamlit as st
import os
import playsound
from gtts import gTTS
import tempfile


def generate(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        filename = tmp.name + '.mp3'
        tts.save(filename)
    return filename



st.title("Text-to-Speech Demo")
st.write("Enter the text you want to hear:")

text = "!"


user_input = st.text_area("Text Input", text)

# Button to trigger speech
if st.button("Speak"):
    if user_input:
        audio = generate(user_input)
        playsound.playsound(audio)
        st.success("Audio played successfully!")

        with open(audio, 'rb') as f:
            st.download_button("Download Audio",f,file_name='audio.mp3',mime='audio/mp3')

    else:
        st.warning("Please enter some text to convert to speech.")
