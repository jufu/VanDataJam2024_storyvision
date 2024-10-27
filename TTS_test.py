import streamlit as st
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from io import BytesIO


client = ElevenLabs(api_key="sk_52760c4684acb397c3909828c1179c065e21cdcacf6815b2")

# Streamlit application layout
st.title("Text-to-Speech with Eleven Labs")
st.write("Enter the text you want to convert to speech:")

# Text input from user
text_input = st.text_area("Text Input", "Try")

if st.button("Generate Audio"):
    if text_input:
        # Define voice settings
        voice = Voice(
            voice_id='XB0fDUnXU5powFXDhCwa',
            settings=VoiceSettings(
                stability=0.5, similarity_boost=0.9, style=0.8, use_speaker_boost=True
            )
        )

        # Generate audio and convert to bytes if it returns a generator
        audio_data = client.generate(text=text_input, voice=voice)
        audio_bytes = b"".join(audio_data)  # Combine generator output into a bytes object

        # Save the audio to a BytesIO object
        audio_file = BytesIO(audio_bytes)
        
        # Use Streamlit to play the audio file
        st.audio(audio_file, format="audio/mp3")

        st.success("Audio generated successfully!")

    else:
        st.warning("Please enter some text to convert to speech.")
