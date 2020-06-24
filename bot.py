import discord
from discord.ext import tasks, commands
from discord.utils import get
import sys
import logging
from cogs.db_operations import db_uwu_check, db_create_serv_data, db_check_serv_data, db_inspass_admin, \
    db_inspass_developper
from loadconfig import is_dev, bot_token_prod, bot_token_dev, developper_id, developper_name

# Initialize ##################################################################################
###############################################################################################

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
bot = commands.Bot(command_prefix=prefix)
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

    if guild.owner.name == developper_name:  # Check if the dev already own the server
        pass
    else:
        # Add the owner of the server as admin
        db_inspass_admin(guild.name, guild.id, guild.owner.name, guild.owner.id)

    # Add the developper as super-admin
    db_inspass_developper(guild.name, guild.id, 'Demokdawa', developper_id)


# Redirect errors and helper menus
@bot.event
async def on_command_error(ctx, message):
    if isinstance(message, commands.MissingRequiredArgument):
        if ctx.command.name == "sendconfig":
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Syntaxe : **__",
                            value="!sendconfig [paramètre] [valeur1] [valeur2] [valeur3]",
                            inline=False)
            embed.add_field(name="__**Liste des paramètres obligatoires**__",
                            value="\n\u200b",
                            inline=False)
            embed.add_field(name="nsfw_mode",
                            value="1 = Désactive le NSFW, 2 = Activé par channel, 3 = Activé sur tout le serveur",
                            inline=False)
            embed.add_field(name="short_reddit_timer",
                            value="Timer court avant la disparition des contenus reddit [4-30s]",
                            inline=False)
            embed.add_field(name="long_reddit_timer",
                            value="Timer long avant la disparition des contenus reddit [10-90s]",
                            inline=False)
            embed.add_field(name="censor_log_channel",
                            value="Nom du channel ou apparaissent les warns",
                            inline=False)
            embed.add_field(name="welcome_channel",
                            value="Nom du channel ou les messages de bienvenue apparaissent",
                            inline=False)
            embed.add_field(name="welcome_role",
                            value="Nom du rôle attribué aux personnes ayant passé la probation",
                            inline=False)
            embed.add_field(name="approb_role",
                            value="Nom du rôle attribué aux personnes n'ayant pas passé la probation [Mee6]",
                            inline=False)
            embed.add_field(name="__**Liste des paramètres facultatifs**__",
                            value="\u200b",
                            inline=False)
            embed.add_field(name="add_nsfw_channel",
                            value="Nom du nouveau channel ou les commandes NSFW seront autorisées",
                            inline=False)
            embed.add_field(name="add_banned_word",
                            value="Ajoute un mot banni, avec possiblité de choisir un remplacant en seconde valeur \n"
                            "Syntaxe : [mot banni] [mot remplacant *facultatif*]",
                            inline=False)
            embed.add_field(name="del_banned_word",
                            value="Supprime un mot banni du serveur \n"
                                  "Syntaxe : [mot banni]",
                            inline=False)
            embed.add_field(name="add_censor_excluded_channel",
                            value="Nom du channel a exclure de la censure textuelle",
                            inline=False)
            embed.add_field(name="add_emoji_role",
                            value="Ajoute un rôle a la personne qui ajoute/supprime un emoji au message "
                                  "ciblé \n"
                            "Syntaxe : [id message suivi] [id emoji] [nom du rôle]",
                            inline=False)
            embed.add_field(name="add_uwu_admin",
                            value="Ajoute un admin UwU sur le serveur \n"
                            "Syntaxe : [id de l'utilisateur] [privilege] \n"
                            "Privilège de niveau 2 (Administrateur) ou 3 (Modérateur)",
                            inline=False)
            embed.add_field(name="del_uwu_admin",
                            value="Supprime un admin UwU sur le serveur \n"
                            "Syntaxe : [id de l'utilisateur] [privilege] \n"
                            "Privilège de niveau 2 (Administrateur) ou 3 (Modérateur)",
                            inline=False)
            await ctx.channel.send(embed=embed)

        if ctx.command.name == "sendwarn":
            pass

    elif isinstance(message, commands.UserInputError):
        await ctx.channel.send(message)
    else:
        log.info(message)


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

if is_dev is True:
    bot.run(bot_token_dev, bot=True, reconnect=True)  # Dev
else:
    bot.run(bot_token_prod, bot=True, reconnect=True)  # Prod

# TO-DO :
# [TEST/ADD] partie gestion admin UwU
# [TEST] commande de showconfig globale et censored
# [TEST] toutes les commandes/menus/checks
# [ADD] les commandes manquantes
# [ADD] la mécanique de goulag
# [ADD] Implementer des features check pour chaque COG
# - Creer une table qui garde l'état d'activation des features (tout est désactivé de base)
# - Désactiver une feature si la configuration est mauvaise
# - Ajouter une commande pour lister ces états
# - Creer des fonctions check pour chaque COG et les lancer avant chaque commande

# [TEST] les commandes de listing pour voir les configurations actuelles
# [MISC] Auto-ajouter le compte "Demokdawa" en level 1 sur tout les serveurs on-join
# [ADD] un système de page si l'affichage dépasse la limite
# [ADD] un MP a Nexx déclenché via emoji
# [ADD] Bloquer l'ajoute du dev en tant qu'admin/modo par les autres users
#
#
# Fix le double message de bienvenue !
# Plus d'utilisations des mentions dans le futur !

# URL d'invitation : https://discord.com/api/oauth2/authorize?client_id=658440750085701662&permissions=268823664&scope=bot

