from discord.ext import tasks, commands
from itertools import zip_longest
from cogs.db_operations import db_get_reddit_command_dict, db_get_reddit_sub_dict, db_get_conf_server_all, \
    db_get_nsfw_channels
import ffmpy
import os
import urllib.request as req
from gfycat.client import GfycatClient
import discord
import random
import asyncio
import functools
import praw
import logging
from loadconfig import reddit_client_id, reddit_client_secret, reddit_user_agent, gfycat_client_id, gfycat_client_secret

# Reddit API infos
reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)

# Retrieve logger
log = logging.getLogger("BlackBot_log")

# Dict to store all submissions
big_dict = {}

# Store the state of the bot (can operate only at 1)
rdy = 0

# Store the progress of the initial cache sync
progress = 0

c_dict = db_get_reddit_command_dict()  # [dict] of commands (dict key is command)
c_dict_sfw = {k: v for k, v in c_dict.items() if v[1] == 0}  # [dict] of SFW commands
c_list_sfw = [(k, v) for k, v in c_dict_sfw.items()]  # [list] of SFW commands
c_dict_nsfw = {k: v for k, v in c_dict.items() if v[1] == 1}  # [dict] of NSFW commands
c_list_nsfw = [(k, v) for k, v in c_dict_nsfw.items()]  # [list] of NSFW commands
c_list = [k for k in c_dict]  # [list] with only commands
sub_dict = db_get_reddit_sub_dict()  # [dict] with subs (dict key is sub)

log.info('[COGS] RedditScrap COG loaded')


# FUNCTIONS ######################################################################################
##################################################################################################


def get_sub_size(sub_size):
    if sub_size >= 10000:
        best = sub_size / 10  # 10%
        return best
    elif sub_size >= 8000:
        best = sub_size / 9  # 11%
        return best
    elif sub_size >= 6000:
        best = sub_size / 9  # 11%
        return best
    elif sub_size >= 4000:
        best = sub_size / 5  # 20%
        return best
    elif sub_size >= 2000:
        best = sub_size / 3  # 33%
        return best
    elif sub_size >= 1000:
        best = sub_size / 1.5  # 66%
        return best
    elif sub_size >= 800:
        best = sub_size / 1.4  # 71%
        return best
    elif sub_size >= 600:
        best = sub_size / 1.4  # 71%
        return best
    elif sub_size >= 400:
        best = sub_size / 1.6  # 62.5%
        return best
    elif sub_size >= 200:
        best = sub_size / 1.35  # 74%
        return best
    elif sub_size >= 100:
        best = sub_size / 1.30  # 76%
        return best
    elif sub_size < 100:
        best = sub_size / 1  # 100%
        return best


def sync_update_cache():
    global big_dict
    global rdy
    global progress

    for sub in sub_dict:
        if sub_dict.get(sub)[2] != '':
            for submission in reddit.subreddit(sub).top(limit=get_sub_size(sub_dict.get(sub)[1])):
                if sub not in big_dict:
                    big_dict[sub_dict.get(sub)[2]] = []
                else:
                    big_dict[sub].append(submission.url)
            progress += 1
        else:
            for submission in reddit.subreddit(sub).top(limit=get_sub_size(sub_dict.get(sub)[1])):
                if sub not in big_dict:
                    big_dict[sub] = []
                else:
                    big_dict[sub].append(submission.url)
            progress += 1
    log.info('Cache update done !')  # INFO
    rdy = 1


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


def get_image(subreddit):
    image_urls = big_dict.get(subreddit)
    print(image_urls)
    random_image = image_urls[random.randint(0, len(image_urls) - 1)]
    log.debug('Chosen content URL is : ' + random_image)  # DEBUG

    if random_image.endswith('.jpg') or random_image.endswith('.png'):
        return random_image, False

    elif random_image.endswith('.gifv'):
        gifed = os.path.splitext(random_image)[0] + '.gif'
        return gifed, True

    elif random_image.endswith('.gif'):
        return random_image, True

    elif 'gfycat' in random_image:
        gyfcat_name = random_image.split(".com/")[1]
        client = GfycatClient(gfycat_client_id, gfycat_client_secret)
        resp = client.query_gfy(gyfcat_name)
        mp4s = resp['gfyItem']['mp4Size']
        mp4f = resp['gfyItem']['mobileUrl']
        mp4nm = resp['gfyItem']['numFrames']
        mp4fr = resp['gfyItem']['frameRate']
        mp4l = mp4nm / mp4fr
        return (mp4s, mp4f, mp4l), True
    else:
        return False, False


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


# DECORATORS #####################################################################################
##################################################################################################


# Decorator to check if reddit bot is ready to serve
def check_if_bot_rdy():
    async def predicate(ctx):
        if rdy == 0:
            await ctx.channel.send("Je suis encore en train de fouiller le web, patiente quelques minutes 😎 ({} / {}) "
                                   .format(progress, len(sub_dict)))
        elif rdy == 1:
            return True

    return commands.check(predicate)


# Decorator to check for NSFW commands
def nsfw_check():
    async def predicate(ctx):
        if c_dict.get(ctx.invoked_with)[1] == 1:  # Check if NSFW command
            if db_get_conf_server_all(ctx.guild.id)[0] == 0:  # Checking current nsfw_mode (disabled)
                await ctx.channel.send("Ey non, pas ici petit coquin ! Ce discord n'est pas NSFW !")
            elif db_get_conf_server_all(ctx.guild.id)[0] == 1:  # Checking current nsfw_mode (semi-enabled)
                if ctx.channel.id in db_get_nsfw_channels(ctx.guild.id):  # If channel is an authorized nsfw channel
                    return True
                else:
                    await ctx.channel.send("Ey non, pas ici petit coquin ! Réessaie dans un channel NSFW !")
            elif db_get_conf_server_all(ctx.guild.id)[0] == 2:  # Checking current nsfw_mode (enable)
                return True
        else:
            return True

    return commands.check(predicate)


# Sanity-check decorator to see if everything config related to this cog is fine
def check_cog_redditscrap():
    async def predicate(ctx):
        conf_server_all = db_get_conf_server_all(ctx.guild.id)
        error_nbr = 0
        if conf_server_all is None:
            raise commands.UserInputError("Ce serveur n\'est pas configuré pour utiliser cette commande !")
        else:
            if not 0 <= conf_server_all[0] <= 2:  # nsfw_mode
                error_nbr += 1
            if not 4 <= conf_server_all[1] <= 30:  # short_reddit_timer
                error_nbr += 1
            if not 10 <= conf_server_all[2] <= 90:  # long_reddit_timer
                error_nbr += 1

            if error_nbr == 0:
                return True
            else:
                await ctx.channel.send("Ce serveur n\'est pas configuré pour utiliser cette commande.\n"
                                       "Configurations erronées/manquantes : {}"
                                       .format(error_nbr))

    return commands.check(predicate)


class RedditScrap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_cache.start()

    # CLASS FUNCTIONS ################################################################################
    ##################################################################################################

    async def check_react(self, ctx, embed, file, isgif):
        await ctx.message.clear_reactions()

        # Change the timer depending if the content is heavy or not
        if isgif is True:
            timer = db_get_conf_server_all(ctx.guild.id)[2]  # Get server specific long-timer reddit value
        else:
            timer = db_get_conf_server_all(ctx.guild.id)[1]  # Get server specific short-timer reddit value

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
            reaction, user = await self.bot.wait_for('reaction_add', timeout=timer, check=check)
        except asyncio.TimeoutError:
            await img.delete()
            await ctx.message.delete()
        else:

            if str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}':
                await img.clear_reactions()
            else:
                await img.delete()
                await ctx.message.delete()

    # COMMANDS #######################################################################################
    ##################################################################################################

    @check_if_bot_rdy()
    @check_cog_redditscrap()
    @nsfw_check()
    @commands.command(aliases=c_list[1:])
    async def sendmeme(self, ctx):
        sub = c_dict.get(ctx.invoked_with)[0]
        await ctx.message.add_reaction('\N{HOURGLASS}')
        data, isgif = get_image(sub)
        while data is False:
            data, isgif = get_image(sub)
        embed, file = prepare_embed(data)
        await self.check_react(ctx, embed, file, isgif)

    # !rcheck to get status of the image-serving service
    @check_cog_redditscrap()
    @commands.command()
    async def rcheck(self, ctx):
        if rdy == 0:
            await ctx.channel.send("Je démarre gros, 2 sec 😎 ({} / {})".format(progress, len(sub_dict)))
        elif rdy == 1:
            await ctx.channel.send("Je suis la pour toi mon chou ❤")

    # !rhelp command for help
    @check_cog_redditscrap()
    @commands.command()
    async def rhelp(self, ctx):

        embed = discord.Embed(title="Bienvenue sur le merveilleux 🤖 des Blackstones !",
                              description="Je suis la pour vous aider 😄", color=0xd5d500)

        embed.set_footer(
            text="Lorsque que vous demandez une image, le bot l'affichera pendant 14 secondes, puis elle "
                 "disparaîtra. \n "
                 "Cliquer sur la réaction ✅ la laissera en permanent. \n Cliquer sur la réaction ❌ supprimera "
                 "l'image "
                 "directement. ")

        if db_get_conf_server_all(ctx.guild.id)[0] == 0:  # Checking current nsfw_mode (disabled)
            for a, b in zip_longest(c_list_sfw[::2], c_list_sfw[1::2]):  # List format to get 1/2 pairs
                if b is not None:
                    embed.add_field(name=a[0], value=b[0], inline=True)
                else:
                    embed.add_field(name=a[0], value='.', inline=True)

        elif db_get_conf_server_all(ctx.guild.id)[0] == 1:  # Checking current nsfw_mode (semi-enabled)
            if ctx.channel.id in db_get_nsfw_channels(ctx.guild.id):  # If channel is an authorized nsfw channel
                for a, b in zip_longest(c_list_nsfw[::2], c_list_nsfw[1::2]):  # # List format to get 1/2 pairs
                    if b is not None:
                        embed.add_field(name=a[0], value=b[0], inline=True)
                    else:
                        embed.add_field(name=a[0], value='.', inline=True)
            else:
                for a, b in zip_longest(c_list_sfw[::2], c_list_sfw[1::2]):
                    if b is not None:
                        embed.add_field(name=a[0], value=b[0], inline=True)
                    else:
                        embed.add_field(name=a[0], value='.', inline=True)

        elif db_get_conf_server_all(ctx.guild.id)[0] == 2:  # Checking current nsfw_mode (enable)
            for a, b in zip_longest(c_list_nsfw[::2], c_list_nsfw[1::2]):  # # List format to get 1/2 pairs
                if b is not None:
                    embed.add_field(name=a[0], value=b[0], inline=True)
                else:
                    embed.add_field(name=a[0], value='.', inline=True)

        await ctx.channel.send(embed=embed)

    # TASKS ##########################################################################################
    ##################################################################################################

    @tasks.loop(seconds=3600)
    async def update_cache(self):
        thing = functools.partial(sync_update_cache)
        await self.bot.loop.run_in_executor(None, thing)


def setup(bot):
    bot.add_cog(RedditScrap(bot))

# For the reddit_scrapping COG : ##
# Improve Gif-conversion system to handle all cases and be flexible
# Get the script async to avoid huge lagtime
# Fix progress counter value being wrong
# Get reddit post values dynamically to DB
# Adds logs to know user statistics
