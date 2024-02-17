from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, generate, voices, play, stream
import os

# client = ElevenLabs(api_key="6bdd0a207a431564f4075147c58d5caf")
os.environ["ELEVEN_API_KEY"] = "6bdd0a207a431564f4075147c58d5caf"

input_folder = 'input-text'
output_folder = 'output-audio'
text_filename = 'induction.txt'
audio_filename = 'induction.mp3'

text_file_path = os.path.join(input_folder, text_filename)
audio_file_path = os.path.join(output_folder, audio_filename)

with open(text_file_path, 'r') as text_file:
  input_text = text_file.read()

audio = generate(text=input_text,
                 api_key='6bdd0a207a431564f4075147c58d5caf',
                 voice=Voice(voice_id='EXAVITQu4vr4xnSDxMaL',
                             settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)),
                 model="eleven_multilingual_v2")

play(audio)

with open(audio_file_path, "wb") as audio_file:
  audio_file.write(audio)
