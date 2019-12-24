import ffmpy
from pygifsicle import gifsicle

ff = ffmpy.FFmpeg(
    inputs={"test.mp4": None},
    outputs={"test.gif": '-r 10 -vf scale=640:360 -b 200k'})

# gifsicle(sources="test.gif", colors=256, options=["-O3", "--lossy=120"])

ff.run()

