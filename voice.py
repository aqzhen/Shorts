# from elevenlabs.client import ElevenLabs
from collections.abc import Iterable

from elevenlabs import Voice, VoiceSettings, generate, voices, play, stream
import os

def text_to_voice(input) -> bytes | Iterable[bytes]:
    # client = ElevenLabs(api_key="6bdd0a207a431564f4075147c58d5caf")
    os.environ["ELEVEN_API_KEY"] = "6bdd0a207a431564f4075147c58d5caf"

    input_folder = 'input-text'

    text_filename = '{}.txt'.format(input)

    text_file_path = os.path.join(input_folder, text_filename)

    with open(text_file_path, 'r') as text_file:
      input_text = text_file.read()

    return generate(text=input_text,
                     api_key='6bdd0a207a431564f4075147c58d5caf',
                     voice=Voice(voice_id='EXAVITQu4vr4xnSDxMaL',
                                 settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)),
                     model="eleven_multilingual_v2")

def write_to_file(audio, output):
    output_folder = 'output-audio'
    audio_filename = '{}.mp3'.format(output)
    audio_file_path = os.path.join(output_folder, audio_filename)

    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio)

audio = text_to_voice('induction')
play(audio)
write_to_file(audio, 'induction')


