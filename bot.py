import discord
import praw
from discord.ext import tasks, commands
import random
import asyncio
import os
from gfycat.client import GfycatClient
import functools


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
                  'ShitPostCrusaders', 'PokePorn', 'wholesomeyaoi', 'PerfectTiming', 'Creepy', 'HentaiVisualArts',
                  'Rule34lol', 'Sukebei']

subreddit_group_hart = ['Artistic_ecchi', 'Artistic_Hentai', 'HentaiVisualArts', 'Sukebei']

big_dict = {}

rdy = 0

progress = 0

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


def sync_update_cache():
    global big_dict
    global rdy
    global progress
    for sub in subreddit_list:
        if sub in subreddit_group_hart:
            for submission in reddit.subreddit(sub).top(limit=1000):
                if 'hart' not in big_dict:
                    big_dict['hart'] = []
                else:
                    big_dict['hart'].append(submission.url)
            progress += 1
        else:
            for submission in reddit.subreddit(sub).top(limit=1000):
                if sub not in big_dict:
                    big_dict[sub] = []
                else:
                    big_dict[sub].append(submission.url)
            progress += 1
    print('Cache update done !')
    rdy = 1


@tasks.loop(seconds=3600)
async def update_cache():
    thing = functools.partial(sync_update_cache)
    await bot.loop.run_in_executor(None, thing)


def check_if_bot_rdy():
    def predicate(ctx):
        if rdy == 0:
            raise commands.UserInputError("Je suis encore en train de récupèrer tes images, patiente quelques minutes 😎 ({} / {}) ".format(progress, len(subreddit_list)))
        if rdy == 1:
            return True
    return commands.check(predicate)


def check_bot_channel():
    def predicate(ctx):
        if ctx.guild.id == 649901370526400522 or ctx.guild.id == 595287360976060577:
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
    print("[Init] Bot en ligne !")
    await bot.change_presence(activity=discord.Game("lel"))


@bot.event
async def on_command_error(ctx, message):
    if isinstance(message, commands.UserInputError):
        await ctx.channel.send(message)

# !sendmeme command for subreddit 'dankmemes'
@bot.command()
@check_if_bot_rdy()
async def sendmeme(ctx):
    data = get_image("dankmemes")
    while data is False:
        data = get_image("dankmemes")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendlewdmeme command for subreddit 'hentaidankmemes'
@bot.command()
@check_if_bot_rdy()
async def sendlewdmeme(ctx):
    data = get_image("hentaidankmemes")
    while data is False:
        data = get_image("hentaidankmemes")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendwfmeme command for subreddit 'memeframe'
@bot.command()
@check_if_bot_rdy()
async def sendwfmeme(ctx):
    data = get_image("memeframe")
    while data is False:
        data = get_image("memeframe")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendcursed command for subreddit 'cursedimages'
@bot.command()
@check_if_bot_rdy()
async def sendcursed(ctx):
    data = get_image("cursedimages")
    while data is False:
        data = get_image("crusedimages")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendyum command for subreddit 'FoodPorn'
@bot.command()
@check_if_bot_rdy()
async def sendyum(ctx):
    data = get_image("FoodPorn")
    while data is False:
        data = get_image("FoodPorn")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendearth command for subreddit 'EarthPorn'
@bot.command()
@check_if_bot_rdy()
async def sendearth(ctx):
    data = get_image("EarthPorn")
    while data is False:
        data = get_image("EarthPorn")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendnocontext command for subreddit 'nocontextpics'        
@bot.command()
@check_if_bot_rdy()
async def sendnocontext(ctx):
    data = get_image("nocontextpics")
    while data is False:
        data = get_image("nocontextpics")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendwtf command for subreddit 'WTF'     
@bot.command()
@check_if_bot_rdy()
async def sendwtf(ctx):
    data = get_image("WTF")
    while data is False:
        data = get_image("WTF")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendaww command for subreddit 'aww'     
@bot.command()
@check_if_bot_rdy()
async def sendaww(ctx):
    data = get_image("aww")
    while data is False:
        data = get_image("aww")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendsfwporn command for subreddit 'SFWporn'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendsfwporn(ctx):
    data = get_image("SFWporn")
    while data is False:
        data = get_image("SFWporn")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendyurimeme command for subreddit 'yurimemes'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendyurimeme(ctx):
    data = get_image("yurimemes")
    while data is False:
        data = get_image("yurimemes")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendyuri command for subreddit 'yuri'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendyuri(ctx):
    data = get_image("yuri")
    while data is False:
        data = get_image("yuri")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendnsfwarframe command for subreddit 'NSFWarframe'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendnsfwarframe(ctx):
    data = get_image("NSFWarframe")
    while data is False:
        data = get_image("NSFWarframe")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendyurigif command for subreddit 'yurigif'     
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendyurigif(ctx):
    data = get_image("yurigif")
    while data is False:
        data = get_image("yurigif")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendhh command for subreddit 'hentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhh(ctx):
    data = get_image("hentai")
    while data is False:
        data = get_image("hentai")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendfurry command for subreddit 'yiff'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendfurry(ctx):
    data = get_image("yiff")
    while data is False:
        data = get_image("yiff")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendneko command for subreddit 'nekogirls'
@bot.command()
@check_if_bot_rdy()
async def sendneko(ctx):
    data = get_image("nekogirls")
    while data is False:
        data = get_image("nekogirls")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendneko command for subreddit 'NekoHentai'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendnekoh(ctx):
    data = get_image("NekoHentai")
    while data is False:
        data = get_image("NekoHentai")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendconfused command for subreddit 'ConfusedBoners'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendconfused(ctx):
    data = get_image("ConfusedBoners")
    while data is False:
        data = get_image("ConfusedBoners")
    embed = prepare_embed(data)
    await check_react(ctx, embed)

# !sendrule command for subreddit 'Rule34'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendrule(ctx):
    data = get_image("Rule34")
    while data is False:
        data = get_image("Rule34")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendhhgif command for subreddit 'Hentai_Gif'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhhgif(ctx):
    data = get_image("Hentai_Gif")
    while data is False:
        data = get_image("Hentai_Gif")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendecchi command for subreddit 'ecchi'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendecchi(ctx):
    data = get_image("ecchi")
    while data is False:
        data = get_image("ecchi")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendjojomeme command for subreddit 'ShitPostCrusaders'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendjojomeme(ctx):
    data = get_image("ShitPostCrusaders")
    while data is False:
        data = get_image("ShitPostCrusaders")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendpokeh command for subreddit 'PokePorn'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendpokeh(ctx):
    data = get_image("PokePorn")
    while data is False:
        data = get_image("PokePorn")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendsoftyaoi command for subreddit 'wholesomeyaoi'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendsoftyaoi(ctx):
    data = get_image("wholesomeyaoi")
    while data is False:
        data = get_image("wholesomeyaoi")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendtiming command for subreddit 'PerfectTiming'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendtiming(ctx):
    data = get_image("PerfectTiming")
    while data is False:
        data = get_image("PerfectTiming")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendcreepy command for subreddit 'Creepy'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendcreepy(ctx):
    data = get_image("Creepy")
    while data is False:
        data = get_image("Creepy")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendhart command for subreddit group Artistic_ecchi + Artistic_Hentai + HentaiVisualArts'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhart(ctx):
    data = get_image("hart")
    while data is False:
        data = get_image("hart")
    embed = prepare_embed(data)
    await check_react(ctx, embed)


# !sendhlol command for subreddit 'Rule34lol'
@bot.command()
@check_if_bot_rdy()
@check_bot_channel()
async def sendhlol(ctx):
    data = get_image("Rule34lol")
    while data is False:
        data = get_image("Rule34lol")
    embed = prepare_embed(data)
    await check_react(ctx, embed)

# !sup to get status of the bot
@bot.command()
async def sup(ctx):
    if rdy == 0:
        await ctx.channel.send("Je démarre gros, 2 sec 😎 ({} / {})".format(progress, len(subreddit_list)))
    if rdy == 1:
        await ctx.channel.send("Je suis la pour toi mon chou !")


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
    embed.add_field(name="!sendhart", value="🔞", inline=False)
    embed.add_field(name="!sendhhgif", value="🔞", inline=False)
    embed.add_field(name="!sendrule", value="🔞", inline=False)
    embed.add_field(name="!sendconfused", value="🔞", inline=False)
    embed.add_field(name="!sendecchi", value="🔞", inline=False)
    embed.add_field(name="!sendfurry", value="🔞", inline=False)
    embed.set_footer(
        text="Lorsque que vous demandez une image, le bot l'affichera pendant 14 secondes, puis elle disparaîtra. \n "
             "Cliquer sur la réaction ✅ la laissera en permanent. \n Cliquer sur la réaction ❌ supprimera l'image "
             "directement. ")
    await ctx.channel.send(embed=embed)


# CumHentai
# AnimatedPorn
# Mariorule34
# Tentai
# Paizuri
# hentaifemdom (a voir)
# need : sub de femdom
# need : sub titsagainsttits

update_cache.start()
bot.run("NjI3MTEwMzM1ODAyNzY5NDA4.XY34wA.ksGsiEaAlgzbZlYVldLSrjivmKM")
