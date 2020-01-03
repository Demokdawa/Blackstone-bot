import ffmpy
from pygifsicle import gifsicle

ff = ffmpy.FFmpeg(
    inputs={"test.mp4": None},
    outputs={"test.gif": '-y -r 9 -vf scale=320:-1'})

# gifsicle(sources="test.gif", colors=256, options=["-O3", "--lossy=120"])

ff.run()

