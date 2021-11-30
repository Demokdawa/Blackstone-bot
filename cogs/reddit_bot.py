from discord.ext import tasks, commands
from itertools import zip_longest
from cogs.db_operations import db_rdt_cmd_data_get, db_get_conf_server_all, db_get_nsfw_channels, \
    db_rdt_rand_content_get, db_rdt_sub_translt_get
import ffmpy
import os
import urllib.request as req
from gfycat.client import GfycatClient
import discord
import random
import asyncio
import functools
import logging
import shortuuid

# Retrieve logger
log = logging.getLogger("General_logs")

c_dict = {items[0]: items[1] for items in db_rdt_cmd_data_get()}  # [dict] of commands (dict key is command)
c_list = [items[0] for items in db_rdt_cmd_data_get()]  # [list] of all commands
c_list_sfw = [items[0] for items in db_rdt_cmd_data_get() if items[1] == 0]  # [list] of SFW commands
c_list_nsfw = [items[0] for items in db_rdt_cmd_data_get() if items[1] == 1]  # [list] of NSFW commands

log.info('[COGS] RedditScrap COG loaded')

# FUNCTIONS ######################################################################################
##################################################################################################


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


def prepare_embed(content_url, content_type):
    # Generate UUID
    data_uid = shortuuid.uuid()

    #if isinstance(content_url, tuple):
    #    log.debug('Prepare embed started / ' + content_url[1] + ' / GFYCAT')  # DEBUG
    #    req.urlretrieve(content_url[1], 'tempDL.mp4')
    #    create_gif(content_url)
    #    file = discord.File(os.path.join(os.getcwd(), "tempDiscord.gif"), filename='tempDiscord.gif')
    #    embed = discord.Embed()
    #    embed.set_image(url="attachment://tempDiscord.gif")

    log.debug('Creating embed for url "' + content_url + '" of type "' + content_type)  # DEBUG
    file = None
    embed = discord.Embed()
    embed.set_image(url=content_url)
    return embed, file


# DECORATORS #####################################################################################
##################################################################################################

# Decorator to check for NSFW commands
def nsfw_check():
    async def predicate(ctx):
        if c_dict.get(ctx.invoked_with) == 1:  # Check if NSFW command
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

    # CLASS FUNCTIONS ################################################################################
    ##################################################################################################

    async def check_react(self, ctx, embed, file, isheavy):
        await ctx.message.clear_reactions()

        # Change the timer depending if the content is heavy or not
        if isheavy is True:
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

    @check_cog_redditscrap()
    @nsfw_check()
    @commands.command(aliases=c_list[1:])
    async def sendmeme(self, ctx):
        sub_tuple = (item for t in db_rdt_sub_translt_get(ctx.invoked_with) for item in t)  # List of subs concerned by command
        await ctx.message.add_reaction('\N{HOURGLASS}')
        content_url, content_type = db_rdt_rand_content_get(sub_tuple)
        log.debug('Chosen content URL is : ' + content_url + ' of type ' + content_type)  # DEBUG
        if content_type in ['gifv', 'gif']:
            isheavy = True
        else:
            isheavy = False
        embed, file = prepare_embed(content_url, content_type)
        await self.check_react(ctx, embed, file, isheavy)

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
                    embed.add_field(name=a[0], value='', inline=True)

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


def setup(bot):
    bot.add_cog(RedditScrap(bot))

# For the reddit_scrapping COG : ##
# Improve Gif-conversion system to handle all cases and be flexible
# Get the script async to avoid huge lagtime
# Adds logs to know user statistics
