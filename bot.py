import discord
import praw
from discord.ext import commands
import random
import urllib.request as req
import os
import time
import asyncio

# Create reddit profile for crawling
reddit = praw.Reddit(client_id='8idC4P5_L45lig', client_secret='yIuMXcbhk7_85syqBj-LF0Uyeb0', user_agent='discord:blackstones (by /u/demo-meme-bot)')

# Set the prefix and init the bot
prefix = "!"
bot = commands.Bot(command_prefix=prefix)
print('[Init] Bot configuré !')

# Remove the default !help command
bot.remove_command('help')


# Check if the bot is ready
@bot.event
async def on_ready():
    print("[Init] Bot en ligne !")
    await bot.change_presence(activity=discord.Game("lel"))


# !sendmeme command for subreddit 'dankmemes'
@bot.command(pass_context=True)
async def sendmeme(ctx):
    subreddit = reddit.subreddit("dankmemes")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
    

# !sendlewdmeme command for subreddit 'hentaidankmemes'
@bot.command()
async def sendlewdmeme(ctx):
    subreddit = reddit.subreddit("hentaidankmemes")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')

    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
        

# !sendwfmeme command for subreddit 'memeframe'
@bot.command()
async def sendwfmeme(ctx):
    subreddit = reddit.subreddit("memeframe")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
        

# !sendcursed command for subreddit 'cursedimages'
@bot.command()
async def sendcursed(ctx):
    subreddit = reddit.subreddit("cursedimages")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()


# !sendyum command for subreddit 'FoodPorn'
@bot.command()
async def sendyum(ctx):
    subreddit = reddit.subreddit("FoodPorn")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
  
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
  
  
# !sendearth command for subreddit 'EarthPorn'
@bot.command()
async def sendearth(ctx):
    subreddit = reddit.subreddit("EarthPorn")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
        

# !sendnocontext command for subreddit 'nocontextpics'        
@bot.command()
async def sendnocontext(ctx):
    subreddit = reddit.subreddit("nocontextpics")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
   
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
        
    
# !sendwtf command for subreddit 'WTF'     
@bot.command()
async def sendwtf(ctx):
    subreddit = reddit.subreddit("WTF")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')

    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
        
    
# !sendaww command for subreddit 'aww'     
@bot.command()
async def sendaww(ctx):
    subreddit = reddit.subreddit("aww")
    image_urls = []
    for submission in subreddit.top(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    req.urlretrieve(random_image, 'tempDiscord.jpg')
    full_path = os.path.join(os.getcwd(), 'tempDiscord.jpg')

    file = discord.File(full_path)
    img = await ctx.channel.send(file=file)
    os.remove('tempDiscord.jpg')
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
        
    
# !react command for testing    
@bot.command()
async def react(ctx):
    msg = await ctx.channel.send("test")
    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await msg.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}']
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await msg.delete()
        await ctx.message.delete()
    else:
        print(reaction)
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await msg.clear_reactions()
        else:
            await msg.delete()
            await ctx.message.delete()
    
    
# !halp command for help
@bot.command()
async def help_command(ctx):
    embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
    embed.add_field(name="Field1", value="hi", inline=False)
    embed.add_field(name="Field2", value="hi2", inline=False)
    await bot.send_message(message.channel, embed=embed)



bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")