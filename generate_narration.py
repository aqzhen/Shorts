# from elevenlabs.client import ElevenLabs
from collections.abc import Iterable

from elevenlabs import Voice, VoiceSettings, generate, voices, play, stream
import os

def text_to_voice(input) -> bytes | Iterable[bytes]:
    # client = ElevenLabs(api_key="6bdd0a207a431564f4075147c58d5caf")

    return generate(text=input,
                     api_key='28a3d454931c95f54351eab642626448',
                     voice=Voice(voice_id='ZJnUinrvqMena46sK7C7',
                                 settings=VoiceSettings(stability=0.30, similarity_boost=0.95, style=0.20, use_speaker_boost=True)),
                     model="eleven_multilingual_v2")

def write_to_file(audio, output):
    output_folder = 'audio'
    audio_filename = '{}.mp3'.format(output)
    audio_file_path = os.path.join(output_folder, audio_filename)

    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio)



