import moviepy.editor as mp
import re
import requests
import os
import base64
from PIL import Image
from io import BytesIO

# need to parse gpt output to list format of
# scenes, narrarations
def parse_generated_output(text):
    # Find all scenes and narrations
    scene_matches = re.findall(r'\[(Scene \d+: .*?|.*?)\]', text)
    narration_matches = re.findall(r'Narrator: "(.*?)"', text, re.DOTALL)

    # Separate scenes and narrations
    scenes = [match for match in scene_matches]
    narrations = [match for match in narration_matches]


    print(narration_matches)


    # Print the extracted scenes and narrations
    return scenes, narrations

def gen_scene_images(scene_texts):
    # call stable diffusion endpoint
    # Replace the empty string with your model id below
    model_id = "6wglrgv3"
    baseten_api_key = "r8CcZACa.92eLpspnkdsYweQDSLSwIKqB3aTeNGpD"
    BASE64_PREAMBLE = "data:image/png;base64,"

    def b64_to_pil(b64_str):
        return Image.open(BytesIO(base64.b64decode(b64_str.replace(BASE64_PREAMBLE, ""))))

    for i, text in enumerate(scene_texts):
        data = {
        "prompt": "Imagine the character is a cartoon animated stick figure, generate a image that describes the character in the following scene : " + text,
        "num_steps": 1,
        }

        # Call model endpoint
        res = requests.post(
            f"https://model-{model_id}.api.baseten.co/production/predict",
            headers={"Authorization": f"Api-Key {baseten_api_key}"},
            json=data
        )

        # Get output image
        res = res.json()
        img_b64 = res.get("result")

        # Save the base64 string to a PNG
        img = b64_to_pil(img_b64)
        img.show()
        img.save(f"./images/image{i}.png")

#def gen_speech_audio(narrations):
    # call elevenlabs api to save to audio folder, naming convention is index of narrations list: audio0, audio1, ...

# now, we have audios and images saved, we can check audio clip length to determine when to show each image
# returns a list of the number of seconds (float) that each image should be on for
def extract_lengths_of_images():
    lengths = []
    import os
    import wave

    # Path to the directory containing image and audio files
    image_dir = "./images"
    audio_dir = "./audio"

    # Iterate over image files
    for image_file in os.listdir(image_dir):
        if image_file.startswith("image"):  # Assuming image files are named image0, image1, etc.
            image_num = image_file[len("image"):].replace(".png", "")
            print(image_num)
            audio_file = f"audio{image_num}.wav"

            # Check if corresponding audio file exists
            audio_path = os.path.join(audio_dir, audio_file)
            if os.path.isfile(audio_path):
                # Open audio file and get its duration
                with wave.open(audio_path, "rb") as audio_wave:
                    audio_duration = audio_wave.getnframes() / audio_wave.getframerate()
                    print(f"Duration of {audio_file}: {audio_duration} seconds")
                    lengths.append(audio_duration)
            else:
                print(f"No corresponding audio file found for {image_file}")
    return lengths
    
def overlay_images():
    video = mp.VideoFileClip("./video/minecraft.mp4")

    image_lengths = extract_lengths_of_images()
    running_sum = 0 
    images = []

    for index in range(len(image_lengths)):
        curr_length = image_lengths[index]
        image = mp.ImageClip(f"./images/image{index}.png").set_start(running_sum).set_duration(curr_length)
        running_sum += curr_length
        images.append(image)

    final = mp.CompositeVideoClip([video] + images)
    final.write_videofile("overlayed.mp4")


def stitch_audio():
    from pydub import AudioSegment
    audio_dir = './audio'
    def extract_number(file_name):
        return int(file_name.split('audio')[1].split('.wav')[0])

    # Get a sorted list of audio file names, ensures in-order iteration
    audio_files = sorted([file_name for file_name in os.listdir(audio_dir) if file_name.startswith("audio") and file_name.endswith(".wav")], key=extract_number)

    sounds = []
    # Iterate over the sorted list of audio files
    for file_name in audio_files:
        # Full path to the audio file
        audio_path = os.path.join(audio_dir, file_name)
        sound = AudioSegment.from_file(audio_path, format="wav")
        sounds.append(sound)

    runningSound = sounds[0] + sounds[1]

    for i in range(2, len(sounds)):
        runningSound = runningSound + sounds[i]


    # simple export
    file_handle = runningSound.export("./audio/stitched_audio.wav", format="wav")


def stitch_movie(audioPath, videoPath):
    audio = mp.AudioFileClip(audioPath) # path to final stitched audio
    video1 = mp.VideoFileClip(videoPath) # path to video with image overlays
    final = video1.set_audio(audio)
    final.write_videofile("result/output.mp4")
