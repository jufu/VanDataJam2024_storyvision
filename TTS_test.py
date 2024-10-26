import streamlit as st
from TTS_test import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs


client = ElevenLabs(
    api_key="sk_52760c4684acb397c3909828c1179c065e21cdcacf6815b2"
)

# Streamlit application layout
st.title("Text-to-Speech with Eleven Labs")
st.write("Enter the text you want to convert to speech:")


text_input = st.text_area("Text Input", "Try")

if st.button("Generate Audio"):
    if text_input:
        audio = client.generate(
            text=text_input,
            voice=Voice(
                voice_id='XB0fDUnXU5powFXDhCwa',
                settings=VoiceSettings(stability=0, similarity_boost=1, style=1, use_speaker_boost=True) #expected to be greater or equal to 0.0 and less or equal to 1.0
            )
        )

        play(audio)
        st.success("Audio generated successfully!")

    
    else:
        st.warning("Please enter some text to convert to speech.")
