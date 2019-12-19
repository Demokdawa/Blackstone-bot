import discord
import praw
from discord.ext import tasks, commands
import random
import time
import asyncio
import os
from gfycat.client import GfycatClient
import aiohttp


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
                  'NekoHentai', 'Hentai_Gif', 'Rule34', 'ConfusedBoners', 'ecchi', 'Artistic_ecchi', 'Artistic_Hentai',
                  'ShitPostCrusaders', 'PokePorn', 'wholesomeyaoi', 'HentaiVisualArts', 'PerfectTiming', 'Creepy']

big_dict = {}


###############################################################################################
# Functions ###################################################################################

def prepare_embed(data):

    embed = discord.Embed()
    embed.set_image(url=data)

    return embed


def get_image(subreddit):

    image_urls = big_dict.get(subreddit)
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    print(random_image)

    if random_image.endswith('.jpg') or random_image.endswith('.png'):
        return random_image

    if random_image.endswith('.gifv'):
        gifed = os.path.splitext(random_image)[0] + '.gif'
        return gifed

    if random_image.endswith('.gif'):
        return random_image

    if 'gfycat' in random_image:
        gyfcat_name = random_image.split(".com/")[1]
        client = GfycatClient('2_I1XC03', 'U6J7oEmkgJ9XYb7UzZ5nrS5nsS-m4-xZLEPAVq3j_s5OcR2AyWa6vHebokbw118L')
        resp = client.query_gfy(gyfcat_name)
        gifed = resp['gfyItem']['gifUrl']
        return gifed

    else:
        return False


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


@tasks.loop(seconds=180)
async def update_cache():
    global big_dict
    async with aiohttp.ClientSession() as cs:
        for sub in subreddit_list:
            temp_list = []
            async with cs.get('https://api.pushshift.io/reddit/search/submission/?subreddit={}&metadata=true&size=1000'.format(sub)) as r:
                res = await r.json()
                for element in res['data']:
                    temp_list.append(element['url'])
            big_dict[sub] = temp_list
    print('Cache update done !')


def update_cache_old():
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
    data = get_image("dankmemes")
    while data is False:
        data = get_image("dankmemes")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendlewdmeme command for subreddit 'hentaidankmemes'
@bot.command()
async def sendlewdmeme(ctx):
    data = get_image("hentaidankmemes")
    while data is False:
        data = get_image("hentaidankmemes")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendwfmeme command for subreddit 'memeframe'
@bot.command()
async def sendwfmeme(ctx):
    data = get_image("memeframe")
    while data is False:
        data = get_image("memeframe")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendcursed command for subreddit 'cursedimages'
@bot.command()
async def sendcursed(ctx):
    data = get_image("cursedimages")
    while data is False:
        data = get_image("crusedimages")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendyum command for subreddit 'FoodPorn'
@bot.command()
async def sendyum(ctx):
    data = get_image("FoodPorn")
    while data is False:
        data = get_image("FoodPorn")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendearth command for subreddit 'EarthPorn'
@bot.command()
async def sendearth(ctx):
    data = get_image("EarthPorn")
    while data is False:
        data = get_image("EarthPorn")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendnocontext command for subreddit 'nocontextpics'        
@bot.command()
async def sendnocontext(ctx):
    data = get_image("nocontextpics")
    while data is False:
        data = get_image("nocontextpics")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendwtf command for subreddit 'WTF'     
@bot.command()
async def sendwtf(ctx):
    data = get_image("WTF")
    while data is False:
        data = get_image("WTF")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendaww command for subreddit 'aww'     
@bot.command()
async def sendaww(ctx):
    data = get_image("aww")
    while data is False:
        data = get_image("aww")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendsfwporn command for subreddit 'SFWporn'     
@bot.command()
async def sendsfwporn(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("SFWporn")
        while data is False:
            data = get_image("SFWporn")
        embed = prepare_embed(data)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendyurimeme command for subreddit 'yurimemes'     
@bot.command()
async def sendyurimeme(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("yurimemes")
        while data is False:
            data = get_image("yurimemes")
        embed = prepare_embed(data)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendyuri command for subreddit 'yuri'     
@bot.command()
async def sendyuri(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("yuri")
        while data is False:
            data = get_image("yuri")
        embed = prepare_embed(data)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendnsfwarframe command for subreddit 'NSFWarframe'     
@bot.command()
async def sendnsfwarframe(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("NSFWarframe")
        while data is False:
            data = get_image("NSFWarframe")
        embed = prepare_embed(data)
        await check_react(ctx, embed)

    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendyurigif command for subreddit 'yurigif'     
@bot.command()
async def sendyurigif(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("yurigif")
        while data is False:
            data = get_image("yurigif")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhh command for subreddit 'hentai'
@bot.command()
async def sendhh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("hentai")
        while data is False:
            data = get_image("hentai")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendfurry command for subreddit 'yiff'
@bot.command()
async def sendfurry(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("yiff")
        while data is False:
            data = get_image("yiff")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendneko command for subreddit 'nekogirls'
@bot.command()
async def sendneko(ctx):
    data = get_image("nekogirls")
    while data is False:
        data = get_image("nekogirls")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendneko command for subreddit 'NekoHentai'
@bot.command()
async def sendnekoh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("NekoHentai")
        while data is False:
            data = get_image("NekoHentai")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendconfused command for subreddit 'ConfusedBoners'
@bot.command()
async def sendconfused(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("ConfusedBoners")
        while data is False:
            data = get_image("ConfusedBoners")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendrule command for subreddit 'Rule34'
@bot.command()
async def sendrule(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("Rule34")
        while data is False:
            data = get_image("Rule34")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhhgif command for subreddit 'Hentai_Gif'
@bot.command()
async def sendhhgif(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("Hentai_Gif")
        while data is False:
            data = get_image("Hentai_Gif")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendecchi command for subreddit 'ecchi'
@bot.command()
async def sendecchi(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("ecchi")
        while data is False:
            data = get_image("ecchi")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendecchiart command for subreddit 'Artistic_ecchi'
@bot.command()
async def sendecchiart(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("Artistic_ecchi")
        while data is False:
            data = get_image("Artistic_ecchi")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhhart command for subreddit 'Artistic_Hentai'
@bot.command()
async def sendhhart(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("Artistic_Hentai")
        while data is False:
            data = get_image("Artistic_Hentai")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendhhart command for subreddit 'Artistic_Hentai'
@bot.command()
async def sendjojomeme(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("ShitPostCrusaders")
        while data is False:
            data = get_image("ShitPostCrusaders")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendpokeh command for subreddit 'PokePorn'
@bot.command()
async def sendpokeh(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("PokePorn")
        while data is False:
            data = get_image("PokePorn")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendsoftyaoi command for subreddit 'wholesomeyaoi'
@bot.command()
async def sendsoftyaoi(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("wholesomeyaoi")
        while data is False:
            data = get_image("wholesomeyaoi")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendlewdart command for subreddit 'HentaiVisualArts'
@bot.command()
async def sendlewdart(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("HentaiVisualArts")
        while data is False:
            data = get_image("HentaiVisualArts")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendtiming command for subreddit 'PerfectTiming'
@bot.command()
async def sendtiming(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("PerfectTiming")
        while data is False:
            data = get_image("PerfectTiming")
        embed = prepare_embed(data)
        await check_react(ctx, embed)
    else:
        await ctx.channel.send("Ey non petit, tu ne peux pas utiliser ca ici !")


# !sendcreepy command for subreddit 'Creepy'
@bot.command()
async def sendcreepy(ctx):
    if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
        data = get_image("Creepy")
        while data is False:
            data = get_image("Creepy")
        embed = prepare_embed(data)
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
    embed.add_field(name="!sendjojomeme", value="Attention aux spoilers !", inline=False)
    embed.add_field(name="!sendneko", value="Envoie des nekos toutes mimi !", inline=False)
    embed.add_field(name="!sendsfwporn", value="🔞", inline=False)
    embed.add_field(name="!sendyuri", value="🔞", inline=False)
    embed.add_field(name="!sendyurigif", value="🔞", inline=False)
    embed.add_field(name="!sendyurimeme", value="🔞", inline=False)
    embed.add_field(name="!sendnsfwarframe", value="🔞", inline=False)
    embed.add_field(name="!sendnekoh", value="🔞", inline=False)
    embed.add_field(name="!sendhh", value="🔞", inline=False)
    embed.add_field(name="!sendhhart", value="🔞", inline=False)
    embed.add_field(name="!sendhhgif", value="🔞", inline=False)
    embed.add_field(name="!sendrule", value="🔞", inline=False)
    embed.add_field(name="!sendconfused", value="🔞", inline=False)
    embed.add_field(name="!sendecchi", value="🔞", inline=False)
    embed.add_field(name="!sendecchiart", value="🔞", inline=False)
    embed.add_field(name="!sendfurry", value="🔞", inline=False)
    embed.set_footer(
        text="Lorsque que vous demandez une image, le bot l'affichera pendant 14 secondes, puis elle disparaîtra. \n "
             "Cliquer sur la réaction ✅ la laissera en permanent. \n Cliquer sur la réaction ❌ supprimera l'image "
             "directement. ")
    await ctx.channel.send(embed=embed)


# CumHentai
# AnimatedPorn
# Rule34lol
# Mariorule34
# Tentai
# Sukebei
# Paizuri
# hentaifemdom (a voir)
# need : sub de femdom
# need : sub titsagainsttits

update_cache.start()
# bot.loop.create_task(task_update_cache(43200))
bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")
