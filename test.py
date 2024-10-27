import torch
import ChatTTS
import torchaudio
from IPython.display import Audio 
import time

start = time.time()

# Initialize ChatTTS

torchaudio.set_audio_backend('soundfile')
chat = ChatTTS.Chat()
chat.load(compile = False)

# Define the text to be converted to speech
text = """
three of the girls [uv_break] has a big smile on her face [laugh], 
and she's nodding her head[laugh] [uv_break] like she's completely 
understanding everything [lbreak] her friend is saying. [laugh]
""".replace('\n', '')  # English is still experimental.

params_refine_text = ChatTTS.Chat.RefineTextParams(
    prompt='[oral_9][laugh_4][break_4]',
)

audio_array_en = chat.infer(text, params_refine_text=params_refine_text)

# Ensure audio_array_en is a 2D tensor before saving
audio_tensor = torch.from_numpy(audio_array_en[0]).unsqueeze(0)  # Add a channel dimension

torchaudio.save("test.wav", audio_tensor, 24000)

end = time.time()

print(end-start)