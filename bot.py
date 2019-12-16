import discord
import praw
from discord.ext import commands
import random
import urllib.request as req
import time
import asyncio
from pygifsicle import gifsicle
import os
from gfycat.client import GfycatClient

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


def prepare_embed(random_image):
    embed = discord.Embed()

    if random_image.endswith('.jpg') or random_image.endswith('.png'):
        embed.set_image(url=random_image)

    if random_image.endswith('.gifv'):
        gifed = os.path.splitext(random_image)[0] + '.gif'
        embed.set_image(url=gifed)

    if random_image.endswith('.gif'):
        embed.set_image(url=random_image)

    if 'gyfcat' in random_image:
        gyfcat_name = random_image.split(".com/")[1]
        client = GfycatClient('2_I1XC03', 'U6J7oEmkgJ9XYb7UzZ5nrS5nsS-m4-xZLEPAVq3j_s5OcR2AyWa6vHebokbw118L')
        resp = client.query_gfy(gyfcat_name)
        gifed = resp['gfyItem']['gifUrl']
        embed.set_image(url=gifed)

    return embed


async def check_react(ctx, embed):
    img = await ctx.channel.send(embed=embed)

    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                             '\N{CROSS MARK}'] and reaction.message.id == img.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:

        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()


# !sendmeme command for subreddit 'dankmemes'
@bot.command(pass_context=True)
async def sendmeme(ctx):
    subreddit = reddit.subreddit("dankmemes")
    image_urls = []
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)

    await check_react(ctx, embed)
    

# !sendlewdmeme command for subreddit 'hentaidankmemes'
@bot.command()
async def sendlewdmeme(ctx):
    subreddit = reddit.subreddit("hentaidankmemes")
    image_urls = []
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)

    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]

    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)
  
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)
   
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try: 
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]

    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)

    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
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
    for submission in subreddit.hot(limit=1000):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            image_urls.append(submission.url)

    random_image = image_urls[random.randint(0,len(image_urls) - 1)]
    
    embed = prepare_embed(random_image)
    
    img = await ctx.channel.send(embed=embed)
    
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try: 
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:
        
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()
            
# !sendsfwporn command for subreddit 'SFWporn'     
@bot.command()
async def sendsfwporn(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("SFWporn")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                image_urls.append(submission.url)

        random_image = image_urls[random.randint(0,len(image_urls) - 1)]
        
        embed = prepare_embed(random_image)
        
        img = await ctx.channel.send(embed=embed)
        
        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:
            
            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")
            
# !sendyurimeme command for subreddit 'yurimemes'     
@bot.command()
async def sendyurimeme(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("yurimemes")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                image_urls.append(submission.url)

        random_image = image_urls[random.randint(0,len(image_urls) - 1)]
        
        embed = prepare_embed(random_image)
        
        img = await ctx.channel.send(embed=embed)
        
        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:
            
            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")
            
            
# !sendyuri command for subreddit 'yuri'     
@bot.command()
async def sendyuri(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("yuri")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
                image_urls.append(submission.url)
                
        print(str(len(image_urls)) + ' submissions found !')

        random_image = image_urls[random.randint(0,len(image_urls) - 1)]
        
        embed = prepare_embed(random_image)
        
        img = await ctx.channel.send(embed=embed)
        
        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:
            
            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")
            
            
# !sendnsfwarframe command for subreddit 'NSFWarframe'     
@bot.command()
async def sendnsfwarframe(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("NSFWarframe")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.jpg') or submission.url.endswith('.png') or submission.url.endswith('.gif'):
                image_urls.append(submission.url)

        random_image = image_urls[random.randint(0,len(image_urls) - 1)]
        
        embed = prepare_embed(random_image)
        
        img = await ctx.channel.send(embed=embed)
        
        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:
            
            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")
        
        
# !sendyurigif command for subreddit 'yurigif'     
@bot.command()
async def sendyurigif(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("yurigif")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.gifv') or submission.url.endswith('.gif') or ('gyfcat' in submission.url):
                image_urls.append(submission.url)

        print(str(len(image_urls)) + ' submissions found !')
        
        random_image = image_urls[random.randint(0,len(image_urls) - 1)]
        
        embed = prepare_embed(random_image)
        
        img = await ctx.channel.send(embed=embed)
        
        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:
            
            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhh command for subreddit 'hentai'
@bot.command()
async def sendhh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("hentai")
        image_urls = []

        start_time_subget = time.time()
        
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.gifv') or submission.url.endswith('.gif') or ('gyfcat' in submission.url):
                image_urls.append(submission.url)

        end_time_subget = time.time()
        print("Get all subs execution time : {}".format(end_time_subget - start_time_subget))

        print(str(len(image_urls)) + ' submissions found !')

        random_image = image_urls[random.randint(0, len(image_urls) - 1)]

        embed = prepare_embed(random_image)

        img = await ctx.channel.send(embed=embed)

        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                                 '\N{CROSS MARK}'] and reaction.message.id == img.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:

            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendfurry command for subreddit 'yiff'
@bot.command()
async def sendfurry(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("yiff")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.gifv') or submission.url.endswith('.gif') or ('gyfcat' in submission.url):
                image_urls.append(submission.url)

        print(str(len(image_urls)) + ' submissions found !')

        random_image = image_urls[random.randint(0, len(image_urls) - 1)]

        embed = prepare_embed(random_image)

        img = await ctx.channel.send(embed=embed)

        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                                 '\N{CROSS MARK}'] and reaction.message.id == img.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:

            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendembed command for subreddit 'yurigif'     
@bot.command()
async def sendembed(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("yurigif")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.gifv') or submission.url.endswith('.gif') or ('gyfcat' in submission.url):
                image_urls.append(submission.url)

        print(str(len(image_urls)) + ' submissions found !')
        
        random_image = image_urls[random.randint(0,len(image_urls) - 1)]
        
        print(random_image)
        
        embed = prepare_embed(random_image)
        
        img = await ctx.channel.send(embed=embed)
            
        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:
            
            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendneko command for subreddit 'nekogirls'
@bot.command()
async def sendneko(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("nekogirls")
        image_urls = []
        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.gifv') or submission.url.endswith('.gif') or ('gyfcat' in submission.url):
                image_urls.append(submission.url)

        print(str(len(image_urls)) + ' submissions found !')

        random_image = image_urls[random.randint(0, len(image_urls) - 1)]

        print(random_image)

        embed = prepare_embed(random_image)

        img = await ctx.channel.send(embed=embed)

        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                                 '\N{CROSS MARK}'] and reaction.message.id == img.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:

            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendneko command for subreddit 'NekoHentai'
@bot.command()
async def sendnekoh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        subreddit = reddit.subreddit("NekoHentai")
        image_urls = []

        start_time_subget = time.time()

        for submission in subreddit.hot(limit=1000):
            if submission.url.endswith('.gifv') or submission.url.endswith('.gif') or ('gyfcat' in submission.url):
                image_urls.append(submission.url)

        end_time_subget = time.time()
        print("Get all subs execution time : {}".format(end_time_subget - start_time_subget))

        print(str(len(image_urls)) + ' submissions found !')

        random_image = image_urls[random.randint(0, len(image_urls) - 1)]

        print(random_image)

        embed = prepare_embed(random_image)

        img = await ctx.channel.send(embed=embed)

        await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await img.add_reaction('\N{CROSS MARK}')

        def check(reaction, user):
            return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                                 '\N{CROSS MARK}'] and reaction.message.id == img.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:

            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !react command for testing
@bot.command()
async def react(ctx):
    msg = await ctx.channel.send("test")
    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await msg.add_reaction('\N{CROSS MARK}')

    def check(reaction, user):
        return user.bot is False and str(reaction.emoji) in ['\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'] and reaction.message.id == img.id
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=14.0, check=check)
    except asyncio.TimeoutError:
        await msg.delete()
        await ctx.message.delete()
    else:
        
        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await msg.clear_reactions()
        else:
            await msg.delete()
            await ctx.message.delete()
    
    
# !halp command for help
@bot.command()
async def halp(ctx):
    embed=discord.Embed(title="Bienvenue sur le merveilleux 🤖 des Blackstones !", description="Je suis la pour vous aider 😄", color=0xd5d500)
    embed.add_field(name="!sendmeme", value="Envoie un dankmeme", inline=False)
    embed.add_field(name="!sendwfmeme", value="Envoie un meme Warframe", inline=False)
    embed.add_field(name="!sencursed", value="Envoie une image maudite", inline=False)
    embed.add_field(name="!sendyum", value="Envoie une image pour te donner faim", inline=False)
    embed.add_field(name="!sendearth", value="Envoie une magnifique image de mère nature", inline=False)
    embed.add_field(name="!sendnocontext", value="Envoie une image sans contexte", inline=False)
    embed.add_field(name="!sendwtf", value="Envoie une image WTF", inline=False)
    embed.add_field(name="!sendaww", value="Envoie des photos d'animaux mignons", inline=False)
    embed.add_field(name="!sendsfwporn", value="Envoie des petits dessins tout mignons !", inline=False)
    embed.add_field(name="!sendyurimeme", value="Euhhhhhhhhh.......", inline=False)
    embed.add_field(name="!sendyuri", value="Mais.........", inline=False)
    embed.add_field(name="!sendyurigif", value="Je crois pas que.....", inline=False)
    embed.add_field(name="!sendnsfwarframe", value="Non, la c'est n'importe quoi !", inline=False)
    embed.add_field(name="!sendneko", value="😵", inline=False)
    embed.add_field(name="!sendnekoh", value="😵", inline=False)
    embed.add_field(name="!sendhh", value="😵", inline=False)
    embed.set_footer(text="Lorsque que vous demandez une image, le bot l'affichera pendant 14 secondes, puis elle disparaîtra. \n Cliquer sur la réaction ✅ la laissera en permanent. \n Cliquer sur la réaction ❌ supprimera l'image directement. ")
    await ctx.channel.send(embed=embed)

# Rule34
# ConfusedBoners
# Hentai
# Hentai_Gif
# Yiff
# SoftHentai
# ecchi
# CumHentai
# nekogirls
# HentaiVisualArts(achecker)

bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")
