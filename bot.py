import discord
import praw
from discord.ext import commands
import asyncio
import random
import urllib.request as req
import os

reddit = praw.Reddit(client_id='8idC4P5_L45lig', client_secret='yIuMXcbhk7_85syqBj-LF0Uyeb0', user_agent='discord:blackstones (by /u/demo-meme-bot)')

prefix = "!"
bot = commands.Bot(command_prefix=prefix)
print('[Init] Bot configuré !')

@bot.event
async def on_ready():
    print("[Init] Bot en ligne !")
    await bot.change_presence(activity=discord.Game("lel"))


@bot.command()
async def sendmeme(ctx):
    subreddit = reddit.subreddit("dankmemes")
    imageUrls = []
    for submission in subreddit.hot(limit=400):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            imageUrls.append(submission.url)

    randomImage = imageUrls[random.randint(0,len(imageUrls) - 1)]
    req.urlretrieve(randomImage, 'tempDiscord.jpg')
    fullPath = os.path.join(os.getcwd(), 'tempDiscord.jpg') 

    file = discord.File(fullPath)
    await ctx.channel.send(file=file)

    os.remove('tempDiscord.jpg')
    
@bot.command()
async def sendlewdmeme(ctx):
    subreddit = reddit.subreddit("hentaidankmemes")
    imageUrls = []
    for submission in subreddit.hot(limit=400):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            imageUrls.append(submission.url)

    randomImage = imageUrls[random.randint(0,len(imageUrls) - 1)]
    req.urlretrieve(randomImage, 'tempDiscord.jpg')
    fullPath = os.path.join(os.getcwd(), 'tempDiscord.jpg') 

    file = discord.File(fullPath)
    await ctx.channel.send(file=file)

    os.remove('tempDiscord.jpg')

   
bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")