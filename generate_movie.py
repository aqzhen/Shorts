import moviepy.editor as mp
import re
import json
import requests
import os
import base64
from PIL import Image
from io import BytesIO
import ast

# need to parse gpt output to list format of
# scenes, narrarations
def parse_generated_output(text):
    # Find all scenes and narrations
    # Parse the JSON string
    if text.endswith("}\n}}"):
        # Remove one '}' character from the end of the string
        text = text[:-1]
    scenes = json.loads(text)

    # Extract the content of each scene into a list
    narrations = [scene["Content"] for scene in scenes.values()]

    # Print the list of content
    # print(len(narrations))

    # Print the extracted scenes and narrations
    return narrations

    # narrations = ast.literal_eval(text)
    # return narrations
    



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
        "prompt": "Generate a concrete image that succintly describes the following scene, focusing on specific items, things, objects, or concepts mentioned : " + text,
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


# now, we have audios and images saved, we can check audio clip length to determine when to show each image
# returns a list of the number of seconds (float) that each image should be on for
def extract_lengths_of_images():
    lengths = []
    import os
    import wave
    from mutagen.mp3 import MP3


    # Path to the directory containing image and audio files
    image_dir = "./images"
    audio_dir = "./audio"

    # Iterate over image files
    for image_file in os.listdir(image_dir):
        if image_file.startswith("image"):  # Assuming image files are named image0, image1, etc.
            image_num = image_file[len("image"):].replace(".png", "")
            print(image_num)
            audio_file = f"audio{image_num}.mp3"

            # Check if corresponding audio file exists
            audio_path = os.path.join(audio_dir, audio_file)
            if os.path.isfile(audio_path):
                # Open audio file and get its duration
                    audio = MP3(audio_path)
                    audio_duration = audio.info.length
                    print(audio_duration)
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
        return int(file_name.split('audio')[1].split('.mp3')[0])

    # Get a sorted list of audio file names, ensures in-order iteration
    audio_files = sorted([file_name for file_name in os.listdir(audio_dir) if file_name.startswith("audio") and file_name.endswith(".mp3")], key=extract_number)

    sounds = []
    # Iterate over the sorted list of audio files
    for file_name in audio_files:
        # Full path to the audio file
        audio_path = os.path.join(audio_dir, file_name)
        sound = AudioSegment.from_file(audio_path, format="mp3")
        sounds.append(sound)

    runningSound = sounds[0] + sounds[1]

    for i in range(2, len(sounds)):
        runningSound = runningSound + sounds[i]


    # simple export
    file_handle = runningSound.export("./audio/stitched_audio.mp3", format="mp3")
# stitch_audio()


def stitch_movie(audioPath, videoPath):
    audio = mp.AudioFileClip(audioPath) # path to final stitched audio
    video1 = mp.VideoFileClip(videoPath) # path to video with image overlays
    final = video1.set_audio(audio)
    final.write_videofile("result/output.mp4")

