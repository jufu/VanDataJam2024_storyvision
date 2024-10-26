from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="sk_52760c4684acb397c3909828c1179c065e21cdcacf6815b2"  # Replace with your actual API key
)

# Function to generate audio
def generate_audio(text):
    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id='XB0fDUnXU5powFXDhCwa',
            settings=VoiceSettings(
                stability=0,
                similarity_boost=0.5,
                style=1,
                use_speaker_boost=True
            )
        )
    )
    return audio

# Example usage
if __name__ == "__main__":
    audio = generate_audio("Hello! My name is Brian.")
    play(audio)
