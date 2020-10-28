from gfycat.client import GfycatClient

gfycat_client_id = '2_I1XC03'
gfycat_client_secret = 'U6J7oEmkgJ9XYb7UzZ5nrS5nsS-m4-xZLEPAVq3j_s5OcR2AyWa6vHebokbw118L'

client = GfycatClient(gfycat_client_id, gfycat_client_secret)

resp = client.query_gfy('pleasingsadhoki')

mp4s = resp['gfyItem']['mp4Size']
mp4f = resp['gfyItem']['mobileUrl']
mp4nm = resp['gfyItem']['numFrames']
mp4fr = resp['gfyItem']['frameRate']
mp4l = mp4nm / mp4fr

print(mp4s, mp4f, mp4nm, mp4fr, mp4l)
