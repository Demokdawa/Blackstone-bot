import discord
from discord.ext import tasks, commands
from discord.utils import get
import sys
import logging
from cogs.db_operations import db_uwu_check, db_create_serv_data, db_check_serv_data, db_inspass_admin, \
    db_inspass_precursor
from loadconfig import is_dev, bot_token_prod, bot_token_dev, precursor_id, precursor_name

# Initialize ##################################################################################
###############################################################################################


# Intents
intents = discord.Intents.default()
intents.members = True


# Common Logger Init
general_logs = logging.getLogger("General_logs")
general_logs.setLevel(logging.DEBUG)
# Poller Logger Init
poller_logs = logging.getLogger("Poller_logs")
poller_logs.setLevel(logging.DEBUG)
# Reddit Logger Init
reddit_logs = logging.getLogger("Reddit_logs")
reddit_logs.setLevel(logging.DEBUG)
# Server moderation Logger Init
moderation_logs = logging.getLogger("Moderation_logs")
moderation_logs.setLevel(logging.DEBUG)

# Console logger for ALL
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
general_logs.addHandler(console)
poller_logs.addHandler(console)
reddit_logs.addHandler(console)
moderation_logs.addHandler(console)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

# File logger for General
fh = logging.FileHandler('logs/General_logs.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
general_logs.addHandler(fh)

# File logger for Poller
fh = logging.FileHandler('logs/Poller_logs.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
poller_logs.addHandler(fh)

# File logger for Reddit
fh = logging.FileHandler('logs/Reddit_logs.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
reddit_logs.addHandler(fh)

# File logger for Moderation
fh = logging.FileHandler('logs/Moderation_logs.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
moderation_logs.addHandler(fh)


# Check DB access
db_uwu_check()

# Cogs variable
initial_extensions = ['cogs.reddit_bot', 'cogs.utils', 'cogs.db_operations', 'cogs.censor_word',
                      'cogs.server_moderation', 'cogs.config_menu', 'cogs.reddit_poller']

# Set the prefix and init the bot
prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.rdy = 0
bot.progress = 0

# Remove the default !help command
bot.remove_command('help')
general_logs.info('BlackBot configuré !')  # INFO


# Check if the bot is ready
@bot.event
async def on_ready():
    if is_dev is True:
        general_logs.info('BlackBot en ligne ! DEVMODE')  # INFO
    else:
        general_logs.info('BlackBot en ligne !')  # INFO
    await bot.change_presence(activity=discord.Game("Lewding.."))


# On guild_join, check server data in DB
@bot.event
async def on_guild_join(guild):
    if db_check_serv_data(guild.id) is True:
        pass
    else:
        db_create_serv_data(guild.name, guild.id)

    if guild.owner.name == precursor_name:  # Check if the dev already own the server
        pass
    else:
        # Add the owner of the server as admin
        db_inspass_admin(guild.name, guild.id, guild.owner.name, guild.owner.id)

    # Add the precursor as super-admin
    db_inspass_precursor(guild.name, guild.id, precursor_name, precursor_id)


# Redirect errors and helper menus of discord.py
@bot.event
async def on_command_error(ctx, message):
    # if isinstance(message, commands.UserInputError):
    #    await ctx.channel.send(message)
    # else:
    #    log.info(message)
    general_logs.info(message)

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

if is_dev is True:
    bot.run(bot_token_dev, bot=True, reconnect=True)  # Dev
else:
    bot.run(bot_token_prod, bot=True, reconnect=True)  # Prod

# TO-DO :
# URGENT ->>
#   REDDIT :
#   Fix le fait que tout les posts ne soient pas récupérés (reddit_poller)
#   MODERATION :
#   Corriger le bug sur les "process_react"
#   Refaire totalement l'ergonomie des commandes de config
#   Ajouter des mentions de config a tout les endroits ou c'est possible

# URL d'invitation : https://discord.com/api/oauth2/authorize?client_id=658440750085701662&permissions=268823664&scope=bot

