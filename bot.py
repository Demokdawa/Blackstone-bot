import discord
import praw
from discord.ext import tasks, commands
import random
import asyncio
import os
from gfycat.client import GfycatClient
import functools
import urllib.request as req
import ffmpy
import logging


# Initialize ##################################################################################

# Enable logging
log = logging.getLogger("BlackBot_log")
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
log.addHandler(console)

fh = logging.FileHandler('Blackbot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d - %(name)s:%(lineno)d - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
log.addHandler(fh)

# Reddit API infos
reddit = praw.Reddit(client_id='8idC4P5_L45lig', client_secret='yIuMXcbhk7_85syqBj-LF0Uyeb0',
                     user_agent='discord:blackstones (by /u/demo-meme-bot)')

# Set the prefix and init the bot
prefix = "!"
bot = commands.Bot(command_prefix=prefix)

# Remove the default !help command
bot.remove_command('help')
log.info('BlackBot configuré !')  # INFO


###############################################################################################
# Config ######################################################################################

# Subreddit dictionnary and size
subreddit_dict = {'dankmemes': 3575074, 'hentaidankmemes': 3960, 'memeframe': 10827, 'cursedimages': 385017,
                  'FoodPorn': 267418, 'EarthPorn': 566895, 'nocontextpics': 34243,
                  'WTF': 2106561, 'aww': 4381771, 'SFWporn': 583, 'yurimemes': 535, 'yuri': 12617, 'NSFWarframe': 1316,
                  'yurigif': 149, 'hentai': 227983, 'yiff': 87178, 'nekogirls': 450,
                  'NekoHentai': 120, 'Hentai_Gif': 15130, 'Rule34': 178548, 'ConfusedBoners': 19627, 'ecchi': 80289,
                  'Artistic_ecchi': 347, 'Artistic_Hentai': 2852,
                  'ShitPostCrusaders': 327045, 'PokePorn': 27740, 'wholesomeyaoi': 1901, 'PerfectTiming': 28848,
                  'Creepy': 249925, 'HentaiVisualArts': 1115, 'Rule34lol': 22897, 'Sukebei': 13893, 'Tentai': 6508,
                  'GloryHo': 904, 'Paizuri': 4322, 'AnimatedPorn': 1921, 'Gifs': 922421, 'WesternHentai': 14521,
                  'hentaifemdom': 5027, 'NintendoWaifus': 17897, 'AnimeBooty': 10168, 'HQHentai': 1025,
                  'thick_hentai': 11141, 'Mariorule34': 2179}

# Subreddit groups for multi-subs commands
subreddit_group_hart = ['Artistic_ecchi', 'Artistic_Hentai', 'HentaiVisualArts', 'Sukebei']

# Dict to store all submissions
big_dict = {}

# Store the state of the bot (can operate only at 1)
rdy = 0

# Store the progress of the initial cache sync
progress = 0

###############################################################################################
# Functions ###################################################################################


def create_gif(data):
    ff1 = ffmpy.FFmpeg(
        inputs={"tempDL.mp4": None},
        outputs={"tempDiscord.gif": '-y -r 12 -loglevel quiet -vf scale=640:-1'})
    ff2 = ffmpy.FFmpeg(
        inputs={"tempDL.mp4": None},
        outputs={"tempDiscord.gif": '-y -r 10 -loglevel quiet -vf scale=640:-1'})
    ff3 = ffmpy.FFmpeg(
        inputs={"tempDL.mp4": None},
        outputs={"tempDiscord.gif": '-y -r 10 -loglevel quiet -vf scale=480:-1'})
    ff4 = ffmpy.FFmpeg(
        inputs={"tempDL.mp4": None},
        outputs={"tempDiscord.gif": '-y -r 10 -loglevel quiet -vf scale=320:-1'})
    ff5 = ffmpy.FFmpeg(
        inputs={"tempDL.mp4": None},
        outputs={"tempDiscord.gif": '-y -r 8 -loglevel quiet -vf scale=320:-1'})

    if data[2] < 10:  # If the gif is less than 10 seconds
        ff1.run()
    else:  # If the gif is more than 10 seconds
        ff2.run()
        if os.path.getsize("tempDiscord.gif") < 8000000:
            pass
        else:
            ff3.run()
            if os.path.getsize("tempDiscord.gif") < 8000000:
                pass
            else:
                ff4.run()
                if os.path.getsize("tempDiscord.gif") < 8000000:
                    pass
                else:
                    ff5.run()


def prepare_embed(data):

    if isinstance(data, tuple):
        log.debug('Prepare embed started / ' + data[1] + ' / GFYCAT')  # DEBUG
        req.urlretrieve(data[1], 'tempDL.mp4')
        create_gif(data)
        file = discord.File(os.path.join(os.getcwd(), "tempDiscord.gif"), filename='tempDiscord.gif')
        embed = discord.Embed()
        embed.set_image(url="attachment://tempDiscord.gif")
    else:
        log.debug('Prepare embed started / ' + data + ' / NOT GFYCAT')  # DEBUG
        file = None
        embed = discord.Embed()
        embed.set_image(url=data)
    return embed, file


def get_image(subreddit):

    image_urls = big_dict.get(subreddit)
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    log.debug('Chosen content URL is : ' + random_image)  # DEBUG

    if random_image.endswith('.jpg') or random_image.endswith('.png'):
        return random_image, False

    if random_image.endswith('.gifv'):
        gifed = os.path.splitext(random_image)[0] + '.gif'
        return gifed, True

    if random_image.endswith('.gif'):
        return random_image, True

    if 'gfycat' in random_image:
        gyfcat_name = random_image.split(".com/")[1]
        client = GfycatClient('2_I1XC03', 'U6J7oEmkgJ9XYb7UzZ5nrS5nsS-m4-xZLEPAVq3j_s5OcR2AyWa6vHebokbw118L')
        resp = client.query_gfy(gyfcat_name)
        mp4s = resp['gfyItem']['mp4Size']
        mp4f = resp['gfyItem']['mobileUrl']
        mp4nm = resp['gfyItem']['numFrames'] 
        mp4fr = resp['gfyItem']['frameRate']
        mp4l = mp4nm / mp4fr
        return (mp4s, mp4f, mp4l), True
    else:
        return False, False


async def check_react(ctx, embed, file, isgif):

    log.debug('React check started...')  # DEBUG

    await ctx.message.clear_reactions()

    # Change the timer depending if the content is heavy or not
    if isgif is True:
        timer = 18
    else:
        timer = 14

    # Check if the embed will contain a file attachement or not
    if file is None:
        img = await ctx.channel.send(embed=embed)
    else:
        img = await ctx.channel.send(file=file, embed=embed)
        
    await img.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await img.add_reaction('\N{CROSS MARK}')

    def check(react, discord_user):
        return discord_user.bot is False and str(react.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                                  '\N{CROSS MARK}'] and react.message.id == img.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=timer, check=check)
    except asyncio.TimeoutError:
        await img.delete()
        await ctx.message.delete()
    else:

        if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
            await img.clear_reactions()
        else:
            await img.delete()
            await ctx.message.delete()


def sync_update_cache():
    global big_dict
    global rdy
    global progress

    def get_sub_nbr(sub_size):
        if sub_size >= 10000:
            best = sub_size / 10  # 10%
            return best
        if sub_size >= 8000:
            best = sub_size / 9  # 11%
            return best
        if sub_size >= 6000:
            best = sub_size / 9  # 11%
            return best
        if sub_size >= 4000:
            best = sub_size / 5  # 20%
            return best
        if sub_size >= 2000:
            best = sub_size / 3  # 33%
            return best
        if sub_size >= 1000:
            best = sub_size / 1.5  # 66%
            return best
        if sub_size >= 800:
            best = sub_size / 1.4  # 71%
            return best
        if sub_size >= 600:
            best = sub_size / 1.4  # 71%
            return best
        if sub_size >= 400:
            best = sub_size / 1.6  # 62.5%
            return best
        if sub_size >= 200:
            best = sub_size / 1.35  # 74%
            return best
        if sub_size >= 100:
            best = sub_size / 1.30  # 76%
            return best
        if sub_size < 100:
            best = sub_size / 1  # 100%
            return best

    for sub in subreddit_dict:
        if sub in subreddit_group_hart:
            for submission in reddit.subreddit(sub).top(limit=get_sub_nbr(subreddit_dict[sub])):
                if 'hart' not in big_dict:
                    big_dict['hart'] = []
                else:
                    big_dict['hart'].append(submission.url)
            progress += 1
        else:
            for submission in reddit.subreddit(sub).top(limit=get_sub_nbr(subreddit_dict[sub])):
                if sub not in big_dict:
                    big_dict[sub] = []
                else:
                    big_dict[sub].append(submission.url)
            progress += 1
    log.info('Cache update done !')  # INFO
    rdy = 1


@tasks.loop(seconds=3600)
async def update_cache():
    thing = functools.partial(sync_update_cache)
    await bot.loop.run_in_executor(None, thing)


def check_if_bot_rdy():
    def predicate(ctx):
        if rdy == 0:
            raise commands.UserInputError("Je suis encore en train de récupèrer tes images, patiente quelques minutes 😎 ({} / {}) ".format(progress, len(subreddit_dict)))
        if rdy == 1:
            return True
    return commands.check(predicate)


def check_bot_channel():
    def predicate(ctx):
        if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577 or ctx.guild.id == 589088834550235156 or ctx.guild.id == 664852715347640320:
            return True
        else:
            raise commands.UserInputError("Ey non, pas ici petit coquin !")
    return commands.check(predicate)

###############################################################################################
# Custom Convertors ###########################################################################


###############################################################################################
# Actuals commands ############################################################################

# Check if the bot is ready
@bot.event
async def on_ready():
    log.info('BlackBot en ligne !')  # INFO
    await bot.change_presence(activity=discord.Game("Lewding.."))


@bot.event
async def on_command_error(ctx, message):
    if isinstance(message, commands.UserInputError):
        await ctx.channel.send(message)


# !sendmeme command for subreddit 'dankmemes'
@bot.command()
@check_if_bot_rdy()
async def sendmeme(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("dankmemes")
    while data is False:
        data, isgif = get_image("dankmemes")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendlewdmeme command for subreddit 'hentaidankmemes'
@bot.command()
@check_if_bot_rdy()
async def sendlewdmeme(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("hentaidankmemes")
    while data is False:
        data, isgif = get_image("hentaidankmemes")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendwfmeme command for subreddit 'memeframe'
@bot.command()
@check_if_bot_rdy()
async def sendwfmeme(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("memeframe")
    while data is False:
        data, isgif = get_image("memeframe")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendcursed command for subreddit 'cursedimages'
@bot.command()
@check_if_bot_rdy()
async def sendcursed(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("cursedimages")
    while data is False:
        data, isgif = get_image("crusedimages")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendyum command for subreddit 'FoodPorn'
@bot.command()
@check_if_bot_rdy()
async def sendyum(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("FoodPorn")
    while data is False:
        data, isgif = get_image("FoodPorn")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendearth command for subreddit 'EarthPorn'
@bot.command()
@check_if_bot_rdy()
async def sendearth(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("EarthPorn")
    while data is False:
        data, isgif = get_image("EarthPorn")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendnocontext command for subreddit 'nocontextpics'        
@bot.command()
@check_if_bot_rdy()
async def sendnocontext(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("nocontextpics")
    while data is False:
        data, isgif = get_image("nocontextpics")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendwtf command for subreddit 'WTF'     
@bot.command()
@check_if_bot_rdy()
async def sendwtf(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("WTF")
    while data is False:
        data, isgif = get_image("WTF")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendaww command for subreddit 'aww'     
@bot.command()
@check_if_bot_rdy()
async def sendaww(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("aww")
    while data is False:
        data, isgif = get_image("aww")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendsfwporn command for subreddit 'SFWporn'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendsfwporn(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("SFWporn")
    while data is False:
        data, isgif = get_image("SFWporn")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendyurimeme command for subreddit 'yurimemes'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendyurimeme(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("yurimemes")
    while data is False:
        data, isgif = get_image("yurimemes")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendyuri command for subreddit 'yuri'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendyuri(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("yuri")
    while data is False:
        data, isgif = get_image("yuri")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendnsfwarframe command for subreddit 'NSFWarframe'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendnsfwarframe(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("NSFWarframe")
    while data is False:
        data, isgif = get_image("NSFWarframe")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendyurigif command for subreddit 'yurigif'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendyurigif(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("yurigif")
    while data is False:
        data, isgif = get_image("yurigif")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhh command for subreddit 'hentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("hentai")
    while data is False:
        data, isgif = get_image("hentai")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendfurry command for subreddit 'yiff'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendfurry(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("yiff")
    while data is False:
        data, isgif = get_image("yiff")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendneko command for subreddit 'nekogirls'
@bot.command()
@check_if_bot_rdy()
async def sendneko(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("nekogirls")
    while data is False:
        data, isgif = get_image("nekogirls")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendneko command for subreddit 'NekoHentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendnekoh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("NekoHentai")
    while data is False:
        data, isgif = get_image("NekoHentai")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendconfused command for subreddit 'ConfusedBoners'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendconfused(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("ConfusedBoners")
    while data is False:
        data, isgif = get_image("ConfusedBoners")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)

# !sendrule command for subreddit 'Rule34'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendrule(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Rule34")
    while data is False:
        data, isgif = get_image("Rule34")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhhgif command for subreddit 'Hentai_Gif'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhhgif(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Hentai_Gif")
    while data is False:
        data, isgif = get_image("Hentai_Gif")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendecchi command for subreddit 'ecchi'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendecchi(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("ecchi")
    while data is False:
        data, isgif = get_image("ecchi")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendjojomeme command for subreddit 'ShitPostCrusaders'
@bot.command()
@check_if_bot_rdy()
async def sendjojomeme(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("ShitPostCrusaders")
    while data is False:
        data, isgif = get_image("ShitPostCrusaders")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendpokeh command for subreddit 'PokePorn'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendpokeh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("PokePorn")
    while data is False:
        data, isgif = get_image("PokePorn")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendsoftyaoi command for subreddit 'wholesomeyaoi'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendsoftyaoi(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("wholesomeyaoi")
    while data is False:
        data, isgif = get_image("wholesomeyaoi")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendtiming command for subreddit 'PerfectTiming'
@bot.command()
@check_if_bot_rdy()
async def sendtiming(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("PerfectTiming")
    while data is False:
        data, isgif = get_image("PerfectTiming")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendcreepy command for subreddit 'Creepy'
@bot.command()
@check_if_bot_rdy()
async def sendcreepy(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Creepy")
    while data is False:
        data, isgif = get_image("Creepy")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhart command for subreddit group Artistic_ecchi + Artistic_Hentai + HentaiVisualArts'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhart(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("hart")
    while data is False:
        data, isgif = get_image("hart")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhlol command for subreddit 'Rule34lol'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhlol(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Rule34lol")
    while data is False:
        data, isgif = get_image("Rule34lol")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)
    
    
# !sendtacles command for subreddit 'Tentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendtacles(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Tentai")
    while data is False:
        data, isgif = get_image("Tentai")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)
    
    
# !sendgho command for subreddit 'GloryHo'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendgho(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("GloryHo")
    while data is False:
        data, isgif = get_image("GloryHo")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendpaizu command for subreddit 'Paizuri'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendpaizu(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Paizuri")
    while data is False:
        data, isgif = get_image("Paizuri")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !send3dh command for subreddit 'AnimatedPorn'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def send3dh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("AnimatedPorn")
    while data is False:
        data, isgif = get_image("AnimatedPorn")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendgif command for subreddit 'Gifs'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendgif(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Gifs")
    while data is False:
        data, isgif = get_image("Gifs")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendwh command for subreddit 'WesternHentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendwh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("WesternHentai")
    while data is False:
        data, isgif = get_image("WesternHentai")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhfemdom command for subreddit 'hentaifemdom'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhfemdom(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("hentaifemdom")
    while data is False:
        data, isgif = get_image("hentaifemdom")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhnwaifu command for subreddit 'NintendoWaifus'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhnwaifu(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("NintendoWaifus")
    while data is False:
        data, isgif = get_image("NintendoWaifus")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhbooty command for subreddit 'AnimeBooty'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhbooty(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("AnimeBooty")
    while data is False:
        data, isgif = get_image("AnimeBooty")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendhqh command for subreddit 'HQHentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhqh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("HQHentai")
    while data is False:
        data, isgif = get_image("HQHentai")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendthickh command for subreddit 'thick_hentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendthickh(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("thick_hentai")
    while data is False:
        data, isgif = get_image("thick_hentai")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sendchampih command for subreddit 'Mariorule34'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendchampih(ctx):
    await ctx.message.add_reaction('\N{HOURGLASS}')
    data, isgif = get_image("Mariorule34")
    while data is False:
        data, isgif = get_image("Mariorule34")
    embed, file = prepare_embed(data)
    await check_react(ctx, embed, file, isgif)


# !sup to get status of the bot
@bot.command()
async def sup(ctx):
    if rdy == 0:
        await ctx.channel.send("Je démarre gros, 2 sec 😎 ({} / {})".format(progress, len(subreddit_dict)))
    if rdy == 1:
        await ctx.channel.send("Je suis la pour toi mon chou !")


# !halp command for help
@bot.command()
async def halp(ctx):
    embed = discord.Embed(title="Bienvenue sur le merveilleux 🤖 des Blackstones !",
                          description="Je suis la pour vous aider 😄", color=0xd5d500)
    embed.add_field(name="!sendmeme", value="!sendwfmeme", inline=True)
    embed.add_field(name="!sencursed", value="!sendyum", inline=True)
    embed.add_field(name="!sendearth", value="!sendnocontext", inline=True)
    embed.add_field(name="!sendnocontext", value="!sendwtf", inline=True)
    embed.add_field(name="!sendaww", value="!sendjojomeme", inline=True)
    embed.add_field(name="!sendneko", value="!sendcreepy", inline=True)
    embed.add_field(name="!sendtiming", value="!sendsfwporn", inline=True)
    embed.add_field(name="!sendyuri", value="!sendyurigif", inline=True)
    embed.add_field(name="!sendyurimeme", value="!sendnsfwarframe", inline=True)
    embed.add_field(name="!sendnekoh", value="!sendhh", inline=True)
    embed.add_field(name="!sendhart", value="!sendhhgif", inline=True)
    embed.add_field(name="!sendrule", value="!sendconfused", inline=True)
    embed.add_field(name="!sendecchi", value="!sendfurry", inline=True)
    embed.add_field(name="!sendhlol", value="!sendpokeh", inline=True)
    embed.add_field(name="!sendsoftyaoi", value="!sendhqh", inline=True)
    embed.add_field(name="!sendhfemdom", value="!sendhnwaifu", inline=True)
    embed.add_field(name="!send3dh", value="!sendwh", inline=True)
    embed.add_field(name="!sendhbooty", value="!sendthickh", inline=True)
    embed.add_field(name="!sendpaizu", value="//", inline=True)
    embed.set_footer(
        text="Lorsque que vous demandez une image, le bot l'affichera pendant 14 secondes, puis elle disparaîtra. \n "
             "Cliquer sur la réaction ✅ la laissera en permanent. \n Cliquer sur la réaction ❌ supprimera l'image "
             "directement. ")
    await ctx.channel.send(embed=embed)


# CumHentai
# need : sub de femdom
# need : sub titsagainsttits

# TO-DO :
# Fix gfycat size (IMPORTANT)
# More commands
# Get the script async to avoid huge lagtime
# Get more submissions than 1000 for huge subs

update_cache.start()
bot.run("NjU4NDQwNzUwMDg1NzAxNjYy.Xf_zWQ.d_a8nNxBy6b7SpA56wQdhsFLJBE")  # Dev
# bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")  # Prod
