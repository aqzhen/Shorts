import moviepy.editor as mp

audio = mp.AudioFileClip("./audio/")
video1 = mp.VideoFileClip('./video/')
final = video1.set_audio(audio)
final.write_videofile("output/output.mp4", codec='mpeg4',
                      audio_codec='libvorbis')
