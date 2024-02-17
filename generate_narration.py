# from elevenlabs.client import ElevenLabs
from collections.abc import Iterable

from elevenlabs import Voice, VoiceSettings, generate, voices, play, stream
import os

def text_to_voice(input) -> bytes | Iterable[bytes]:
    # client = ElevenLabs(api_key="6bdd0a207a431564f4075147c58d5caf")

    return generate(text=input,
                     api_key='3dbf7f2ff3ff5a5db94e5147f35951c0',
                     voice=Voice(voice_id='qhEds1nihpGHlVvSOuSW',
                                 settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)),
                     model="eleven_multilingual_v2")

def write_to_file(audio, output):
    output_folder = 'audio'
    audio_filename = '{}.mp3'.format(output)
    audio_file_path = os.path.join(output_folder, audio_filename)

    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio)



