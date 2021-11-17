# Need to be implemented inside poller to write correct Gfycat old NSFW links

import requests
import shortuuid
from pathlib import Path
from videoprops import get_video_properties
from bs4 import BeautifulSoup

INPUT_CONTENT_URL = "https://gfycat.com/deadsoulfulaegeancat"

# Get last part of URL with ID
gif_id = INPUT_CONTENT_URL.split("/")[-1]

redgif_url = "https://www.redgifs.com/watch/{}".format(gif_id)

r = requests.get(redgif_url)
soup = BeautifulSoup(r.content, "html.parser")

data = soup.find("meta", property="og:video")

print(data["content"])

video_url = data["content"]

# Generate UUID for temp vid file
temp_mp4_name = shortuuid.uuid() + ".mp4"

# Temporary folder path
temp_mp4_folder = Path("temp/")

# Downloading video and writing to file
r = requests.get(video_url, allow_redirects=True)
open(temp_mp4_folder / temp_mp4_name, 'wb').write(r.content)

props = get_video_properties("temp/DCiURfD593WKbyaGPuYMsY.mp4")
print(f'''
Width : {props['width']}
Height : {props['height']}
FPS : {props['avg_frame_rate']}
Duration : {props['duration']}
BitDepth : {props['bits_per_raw_sample']}
''')

# Data needed for gif conversion
# Heigh
# Widht
# FPS
# Duration
# BitDepth

# NEXT THINGS TO DEV TO RE-IMPLEMENT GIFS :
# 1. Check to gfycat links to know if it's a wrong redgif link or not (and do above process in first case)
# 2. Regular checks on every format (gif, gifv, img, jpg, png and gfycat/redgif) if the URL is not dead
# 3. Check if new implementation of poller is working correctly and getting everything right
# 4. Better and faster gif compression
# 5. Check why black squares occur and fix



