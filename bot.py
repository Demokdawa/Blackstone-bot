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


# Enable logger
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

# Check DB access
db_uwu_check()

# Cogs variable
initial_extensions = ['cogs.reddit_scrap', 'cogs.utils', 'cogs.db_operations', 'cogs.censor_word',
                      'cogs.server_moderation', 'cogs.config_menu']

# Set the prefix and init the bot
prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.rdy = 0
bot.progress = 0

# Remove the default !help command
bot.remove_command('help')
log.info('BlackBot configuré !')  # INFO


# Check if the bot is ready
@bot.event
async def on_ready():
    if is_dev is True:
        log.info('BlackBot en ligne ! DEVMODE')  # INFO
    else:
        log.info('BlackBot en ligne !')  # INFO
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
    db_inspass_precursor(guild.name, guild.id, 'Demokdawa', precursor_id)


# Redirect errors and helper menus of discord.py
@bot.event
async def on_command_error(ctx, message):
    # if isinstance(message, commands.UserInputError):
    #    await ctx.channel.send(message)
    # else:
    #    log.info(message)
    log.info(message)

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
#   Fix le bug sur les groupes pour le reddiscrap
#   Migrer de praw a json api
#   Faire en sorte de récuperer les chiffres du nombre de post reddit pour mieux calculer
#   MODERATION :
#   Corriger le bug sur les "process_react"
#   Refaire totalement l'ergonomie des commandes de config
#   Ajouter des mentions de config a tout les endroits ou c'est possible

# URL d'invitation : https://discord.com/api/oauth2/authorize?client_id=658440750085701662&permissions=268823664&scope=bot

