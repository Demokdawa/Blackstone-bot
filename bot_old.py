import discord
from discord.ext import tasks, commands
from discord.utils import get
import praw
import functools
import logging
import sqlite3


db_check(log)

# Reddit API infos
reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)

# Set the prefix and init the bot
prefix = "!"
bot = commands.Bot(command_prefix=prefix)
bot.log = log

# Remove the default !help command
bot.remove_command('help')
log.info('BlackBot configuré !')  # INFO

# Connect to sqlite3
db = sqlite3.connect('blackbotdb.sqlite3')

###############################################################################################
# Config ######################################################################################

# Dict to store all submissions
big_dict = {}

# Store the state of the bot (can operate only at 1)
rdy = 0

# Store the progress of the initial cache sync
progress = 0

# Store the curse words and their replacement


###############################################################################################
# Rôle Attribution ############################################################################

@bot.event
async def on_raw_reaction_add(payload):
    message_to_track = 688008749775978506

    mc_emoji = 687352522612146193
    teso_emoji = 687352522318675975
    lol_emoji = 687352522159292456
    mhw_emoji = 687352521756639268
    ark_emoji = 687352517738233909
    wf_emoji = 481419061662842880
    fps_emoji = 687789203727188063

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    mc = get(guild.roles, id=519147063985045504)
    teso = get(guild.roles, id=410552777580871681)
    lol = get(guild.roles, id=410552805657411591)
    mhw = get(guild.roles, id=458249750475702284)
    ark = get(guild.roles, id=572822480813817868)
    warframe = get(guild.roles, id=410552725168848896)
    fps = get(guild.roles, id=687275506432737320)

    new_member = get(guild.roles, id=687282300672540715)
    silencieux = get(guild.roles, id=415554374056673301)

    list_of_user_roles = [e.id for e in member.roles]

    channel = bot.get_channel(368464196008148992)

    if payload.message_id == message_to_track:
        if 687282300672540715 in list_of_user_roles:
            if payload.emoji.id == mc_emoji:
                await member.add_roles(mc, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif payload.emoji.id == teso_emoji:
                await member.add_roles(teso, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif payload.emoji.id == lol_emoji:
                await member.add_roles(lol, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif payload.emoji.id == mhw_emoji:
                await member.add_roles(mhw, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif payload.emoji.id == ark_emoji:
                await member.add_roles(ark, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif payload.emoji.id == wf_emoji:
                await member.add_roles(warframe, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif payload.emoji.id == fps_emoji:
                await member.add_roles(warframe, silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')

        else:
            if payload.emoji.id == mc_emoji:
                await member.add_roles(mc, reason=None, atomic=True)
            elif payload.emoji.id == teso_emoji:
                await member.add_roles(teso, reason=None, atomic=True)
            elif payload.emoji.id == lol_emoji:
                await member.add_roles(lol, reason=None, atomic=True)
            elif payload.emoji.id == mhw_emoji:
                await member.add_roles(mhw, reason=None, atomic=True)
            elif payload.emoji.id == ark_emoji:
                await member.add_roles(ark, reason=None, atomic=True)
            elif payload.emoji.id == fps_emoji:
                await member.add_roles(fps, reason=None, atomic=True)
            elif payload.emoji.id == wf_emoji:
                await member.add_roles(warframe, reason=None, atomic=True)


@bot.event
async def on_raw_reaction_remove(payload):
    message_to_track = 688008749775978506

    mc_emoji = 687352522612146193
    teso_emoji = 687352522318675975
    lol_emoji = 687352522159292456
    mhw_emoji = 687352521756639268
    ark_emoji = 687352517738233909
    wf_emoji = 481419061662842880
    fps_emoji = 687789203727188063

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    mc = get(guild.roles, id=519147063985045504)
    teso = get(guild.roles, id=410552777580871681)
    lol = get(guild.roles, id=410552805657411591)
    mhw = get(guild.roles, id=458249750475702284)
    ark = get(guild.roles, id=572822480813817868)
    warframe = get(guild.roles, id=410552725168848896)
    fps = get(guild.roles, id=687275506432737320)

    if payload.message_id == message_to_track:
        if payload.emoji.id == mc_emoji:
            await member.remove_roles(mc, reason=None, atomic=True)
        elif payload.emoji.id == teso_emoji:
            await member.remove_roles(teso, reason=None, atomic=True)
        elif payload.emoji.id == lol_emoji:
            await member.remove_roles(lol, reason=None, atomic=True)
        elif payload.emoji.id == mhw_emoji:
            await member.remove_roles(mhw, reason=None, atomic=True)
        elif payload.emoji.id == ark_emoji:
            await member.remove_roles(ark, reason=None, atomic=True)
        elif payload.emoji.id == fps_emoji:
            await member.remove_roles(fps, reason=None, atomic=True)
        elif payload.emoji.id == wf_emoji:
            await member.remove_roles(warframe, reason=None, atomic=True)


###############################################################################################
# Image-Serving Commands ######################################################################


# Check if the bot is ready
@bot.event
async def on_ready():
    if is_dev is True:
        log.info('BlackBot en ligne ! DEVMODE')  # INFO
    else:
        log.info('BlackBot en ligne !')  # INFO
    await bot.change_presence(activity=discord.Game("Lewding.."))


#@bot.event
#async def on_command_error(ctx, message):
#    if isinstance(message, commands.UserInputError):
#        await ctx.channel.send(message)
#    else:
#        log.info(message)



        
###############################################################################################
# Others commands #############################################################################

# !warn [pseudo] command to warn a specific user
@bot.command()
async def warn(ctx, a1):
    mentionned_id = ctx.message.mentions[0].id
    cursor = db.cursor()
    # TestQuery
    cursor.execute('''SELECT IDUser FROM Users WHERE DiscordUserId = ?''', (ctx.message.mentions[0].id,))
    result = cursor.fetchone()
    if result:
        cursor.execute('''UPDATE Users SET WarnsNumber = WarnsNumber + 1 WHERE DiscordUserId = ?''', (ctx.message.mentions[0].id,))
    else:
        cursor.execute('''INSERT INTO Users (DiscordUserId, DiscordUserTag, WarnsNumber) VALUES (?,?,?)''', (ctx.message.mentions[0].id, str(ctx.message.author), 1))
    db.commit()
    print(ctx.message.mentions[0])
    await ctx.channel.send(str(mentionned_id) + ' is warned !')
    



# TO-DO :
# Improve Gif-conversion system to handle all cases and be flexible
# Get the script async to avoid huge lagtime
# Fix progress counter value being wrong
# Fix double welcome message
# Get reddit post values dynamically
# Change all bot config to dynamic
# Adds logs to know user statistics

if __name__ == '__bot__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            raise


# update_cache.start()
if is_dev is True:
    bot.run(bot_token_dev, bot=True, reconnect=True)  # Dev
else:
    bot.run(bot_token_prod, bot=True, reconnect=True)  # Prod
