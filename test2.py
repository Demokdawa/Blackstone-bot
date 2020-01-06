import ffmpy
import os

ff = ffmpy.FFmpeg(
    inputs={"test2.mp4": None},
    outputs={"test2.gif": '-y -r 40 -loglevel quiet -vf scale=640:-1'})
ff.run()

if os.path.getsize("test2.gif") < 8000000:
	print("All good")
else:
	ff = ffmpy.FFmpeg(
    inputs={"test2.mp4": None},
    outputs={"test2.gif": '-y -r 10 -loglevel quiet -vf scale=320:-1'})
	ff.run()




