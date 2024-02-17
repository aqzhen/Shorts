import moviepy.editor as mp


def stitch_movie(audioPath, videoPath):
    audio = mp.AudioFileClip(audioPath)
    video1 = mp.VideoFileClip(videoPath)
    final = video1.set_audio(audio)
    final.write_videofile("output/output.mp4", codec='mpeg4',
                        audio_codec='libvorbis')
