import discord
import praw
from discord.ext import commands
import random
# import urllib.request as req
import time
import asyncio
# from pygifsicle import gifsicle
import os
from gfycat.client import GfycatClient


# Initialize ##################################################################################
reddit = praw.Reddit(client_id='8idC4P5_L45lig', client_secret='yIuMXcbhk7_85syqBj-LF0Uyeb0',
                     user_agent='discord:blackstones (by /u/demo-meme-bot)')

# Set the prefix and init the bot
prefix = "!"
bot = commands.Bot(command_prefix=prefix)

# Remove the default !help command
bot.remove_command('help')
print('[Init] Bot configuré !')


###############################################################################################
# Config ######################################################################################

subreddit_list = ['dankmemes', 'hentaidankmemes', 'memeframe', 'cursedimages', 'FoodPorn', 'EarthPorn', 'nocontextpics',
                  'WTF', 'aww', 'SFWporn', 'yurimemes', 'yuri', 'NSFWarframe', 'yurigif', 'hentai', 'yiff', 'nekogirls',
                  'nekohentai', 'Hentai_Gif', 'Rule34', 'ConfusedBoners']

big_dict = {}


###############################################################################################
# Functions ###################################################################################

def prepare_embed(random_image):
    print(random_image)
    embed = discord.Embed()

    if random_image.endswith('.jpg') or random_image.endswith('.png'):
        embed.set_image(url=random_image)

    if random_image.endswith('.gifv'):
        gifed = os.path.splitext(random_image)[0] + '.gif'
        embed.set_image(url=gifed)

    if random_image.endswith('.gif'):
        embed.set_image(url=random_image)

    if 'gfycat' in random_image:
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

    def check(react, discord_user):
        return discord_user.bot is False and str(react.emoji) in ['\N{WHITE HEAVY CHECK MARK}',
                                                                  '\N{CROSS MARK}'] and react.message.id == img.id

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


def update_cache():
    global big_dict
    for sub in subreddit_list:
        temp_list = []
        for submission in reddit.subreddit(sub).top(limit=1000):
            temp_list.append(submission.url)
        big_dict[sub] = temp_list
    print('Cache update done !')


###############################################################################################
# Background Tasks ############################################################################


async def task_update_cache(timeout):
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            update_cache()
            await asyncio.sleep(timeout)
        except Exception as e:
            print(str(e))
            await asyncio.sleep(timeout)


###############################################################################################
# Custom Convertors ###########################################################################


###############################################################################################
# Actuals commands ############################################################################

# Check if the bot is ready
@bot.event
async def on_ready():
    print("[Init] Bot en ligne !")
    await bot.change_presence(activity=discord.Game("lel"))

# !sendmeme command for subreddit 'dankmemes'
@bot.command()
async def sendmeme(ctx):
    image_urls = big_dict.get("dankmemes")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendlewdmeme command for subreddit 'hentaidankmemes'
@bot.command()
async def sendlewdmeme(ctx):
    image_urls = big_dict.get("hentaidankmemes")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendwfmeme command for subreddit 'memeframe'
@bot.command()
async def sendwfmeme(ctx):
    image_urls = big_dict.get("memeframe")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendcursed command for subreddit 'cursedimages'
@bot.command()
async def sendcursed(ctx):
    image_urls = big_dict.get("cursedimages")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendyum command for subreddit 'FoodPorn'
@bot.command()
async def sendyum(ctx):
    image_urls = big_dict.get("FoodPorn")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendearth command for subreddit 'EarthPorn'
@bot.command()
async def sendearth(ctx):
    image_urls = big_dict.get("EarthPorn")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendnocontext command for subreddit 'nocontextpics'        
@bot.command()
async def sendnocontext(ctx):
    image_urls = big_dict.get("nocontextpics")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendwtf command for subreddit 'WTF'     
@bot.command()
async def sendwtf(ctx):
    image_urls = big_dict.get("WTF")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendaww command for subreddit 'aww'     
@bot.command()
async def sendaww(ctx):
    image_urls = big_dict.get("aww")
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendsfwporn command for subreddit 'SFWporn'     
@bot.command()
async def sendsfwporn(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("SFWporn")
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendyurimeme command for subreddit 'yurimemes'     
@bot.command()
async def sendyurimeme(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("yurimemes")
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendyuri command for subreddit 'yuri'     
@bot.command()
async def sendyuri(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("yuri")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendnsfwarframe command for subreddit 'NSFWarframe'     
@bot.command()
async def sendnsfwarframe(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("NSFWarframe")
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendyurigif command for subreddit 'yurigif'     
@bot.command()
async def sendyurigif(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("yurigif")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhh command for subreddit 'hentai'
@bot.command()
async def sendhh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("hentai")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendfurry command for subreddit 'yiff'
@bot.command()
async def sendfurry(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("yiff")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendneko command for subreddit 'nekogirls'
@bot.command()
async def sendneko(ctx):
    image_urls = big_dict.get("nekogirls")
    print(str(len(image_urls)) + ' submissions found !')
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    embed = prepare_embed(random_image)
    await check_react(ctx, embed)


# !sendneko command for subreddit 'NekoHentai'
@bot.command()
async def sendnekoh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("NekoHentai")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendconfused command for subreddit 'ConfusedBoners'
@bot.command()
async def sendconfused(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("ConfusedBoners")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendrule command for subreddit 'Rule34'
@bot.command()
async def sendrule(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("Rule34")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhhgif command for subreddit 'Hentai_Gif'
@bot.command()
async def sendhhgif(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        image_urls = big_dict.get("Hentai_Gif")
        print(str(len(image_urls)) + ' submissions found !')
        random_image = image_urls[random.randint(0, len(image_urls) - 1)]
        embed = prepare_embed(random_image)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !halp command for help
@bot.command()
async def halp(ctx):
    embed = discord.Embed(title="Bienvenue sur le merveilleux 🤖 des Blackstones !",
                          description="Je suis la pour vous aider 😄", color=0xd5d500)
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
    embed.set_footer(
        text="Lorsque que vous demandez une image, le bot l'affichera pendant 14 secondes, puis elle disparaîtra. \n "
             "Cliquer sur la réaction ✅ la laissera en permanent. \n Cliquer sur la réaction ❌ supprimera l'image "
             "directement. ")
    await ctx.channel.send(embed=embed)


# SoftHentai
# ecchi
# CumHentai
# HentaiVisualArts(achecker)

bot.loop.create_task(task_update_cache(7200))
bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")
