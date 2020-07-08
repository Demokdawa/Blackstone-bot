import discord
from discord.ext import tasks, commands
from discord.utils import get
import logging
from cogs.utils import chk_arg1_sndcfg, chk_arg1_shcfg, check_if_owner, admin_restricted
from cogs.db_operations import db_insup_value, db_check_privilege, db_insupdel_admin, db_get_conf_server_all, \
    db_get_censor_words, db_get_excl_channels, db_get_server_emoji_roles, db_get_nsfw_channels, db_del_value

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] ConfigMenu COG loaded')


# DECORATORS #####################################################################################
##################################################################################################

class ConfigMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command that call db insert/update function to modify/add configs to the DB
    # Arg1 = param name, Arg2 = Value of config, Arg* = Others values of config
    @admin_restricted()
    @commands.command()
    async def sendconfig(self, ctx, arg1: chk_arg1_sndcfg, arg2=None, arg3=None, arg4=None):

        if arg1 == 'nsfw_mode':  # GOOD
            if arg2 is None or arg2 != "reset" and not arg2.isdigit() or arg2.isdigit() and not 0 <= int(arg2) <= 2:
                await ctx.channel.send(
                    "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 0 et 2 requis ou 'reset')"
                    .format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, arg2))
                if arg2 == "reset":
                    await ctx.channel.send("Remise a zéro du mode NSFW effectuée !")
                else:
                    await ctx.channel.send("Mode NSFW modifé avec succès : **{}**".format(arg2))
        ##
        elif arg1 == 'short_reddit_timer':  # GOOD
            if arg2 is None or arg2 != "reset" and not arg2.isdigit or arg2.isdigit() and not 4 <= int(arg2) <= 30:
                await ctx.channel.send(
                    "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 4 et 30 requis, ou 'reset')"
                    .format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, arg2))
                if arg2 == "reset":
                    await ctx.channel.send("Remise a zéro du timer effectuée !")
                else:
                    await ctx.channel.send("Timer modifié avec succès : **{}**".format(arg2))
        ##
        elif arg1 == 'long_reddit_timer':  # GOOD
            if arg2 is None or arg2 != "reset" and not arg2.isdigit or arg2.isdigit() and not 10 <= int(arg2) <= 90:
                await ctx.channel.send(
                    "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 10 et 90 requis ou 'reset')"
                    .format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, arg2))
                if arg2 == "reset":
                    await ctx.channel.send("Remise a zéro du timer effectuée !")
                else:
                    await ctx.channel.send("Timer modifié avec succès : **{}**".format(arg2))
        ##
        elif arg1 in ['censor_log_channel', 'welcome_channel']:  # GOOD
            channel_obj = get(ctx.guild.channels, name=arg2)
            if channel_obj is None and arg2 != "reset":
                await ctx.channel.send(
                    "Ce channel n'existe pas (vous pouvez aussi entrer 'reset') : **{}** [Arg 2]"
                    .format(arg2))
            elif arg2 == "reset":
                db_insup_value(arg1, (ctx.guild.id, "reset"))
                await ctx.channel.send("Remise a zéro du channel effectuée ! : **{}** [Arg 2]".format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, channel_obj.id))
                await ctx.channel.send("Channel ajouté avec succés ! : **{}** [Arg 2]".format(arg2))
        ##
        elif arg1 in ['add_nsfw_channel', 'add_censor_excluded_channel']:  # GOOD
            channel_obj = get(ctx.guild.channels, name=arg2)
            if channel_obj is None:
                await ctx.channel.send(
                    "Ce channel n'existe pas (vous pouvez aussi entrer 'reset') : **{}** [Arg 2]"
                    .format(arg2))
            else:
                res = db_insup_value(arg1, (ctx.guild.id, ctx.guild.name, channel_obj.id, channel_obj.name))
                if res is False:
                    await ctx.channel.send("Ce channel est déja configuré pour cela : **{}** [Arg 2]".format(arg2))
                else:
                    await ctx.channel.send("Channel correctement ajouté ! : **{}** [Arg 2]".format(arg2))
        ##
        elif arg1 in ['del_nsfw_channel', 'del_censor_excluded_channel']:  # GOOD
            channel_obj = get(ctx.guild.channels, name=arg2)
            if channel_obj is None:
                await ctx.channel.send(
                    "Ce channel n'existe pas : **{}** [Arg 2]"
                    .format(arg2))
            else:
                db_del_value(arg1, (ctx.guild.id, channel_obj.id))
                await ctx.channel.send("Channel correctement supprimé ! : **{}** [Arg 2]".format(arg2))
        ##
        elif arg1 == 'welcome_role' or arg1 == 'approb_role':  # GOOD
            role_obj = get(ctx.guild.roles, name=arg2)
            if role_obj is None and arg2 != "reset":
                await ctx.channel.send(
                    "Ce rôle n'existe pas : **{}** [Arg 2]"
                    .format(arg2))
            elif arg2 == "reset":
                db_insup_value(arg1, (ctx.guild.id, "reset"))
                await ctx.channel.send("Remise a zéro du role effectuée !")
            else:
                db_insup_value(arg1, (ctx.guild.id, role_obj.id))
                await ctx.channel.send("Role modifié avec succès ! : **{}** [Arg 2]".format(arg2))
        ##
        elif arg1 == 'add_banned_word':  # GOOD
            db_insup_value(arg1, (ctx.guild.id, ctx.guild.name, arg2, arg3))
        ##
        elif arg1 == 'del_banned_word':  # GOOD
            db_del_value(arg1, (ctx.guild.id, arg2))
        ##
        elif arg1 == 'add_emoji_role':
            if not arg2.isdigit() or arg2 is None:
                await ctx.channel.send("Paramètre manquant / incorrect : **{}** [Arg 2]".format(arg2))
            else:
                if not arg3.isdigit() or arg3 is None:
                    await ctx.channel.send("Paramètre manquant / incorrect : **{}** [Arg 3]".format(arg3))
                else:
                    role_obj = get(ctx.guild.roles, name=arg4)
                    if role_obj is None:
                        await ctx.channel.send(
                            "Ce rôle n'existe pas ou n'est pas correctement renseigné : **{}** [Arg 4]"
                            .format(arg4))
                    else:
                        db_insup_value(arg1, (ctx.guild.id, ctx.guild.name, arg4, int(arg2), int(arg3), role_obj.id))
        ##
        elif arg1 == 'del_emoji_role':
            if not arg2.isdigit() or arg2 is None:
                await ctx.channel.send("Paramètre manquant / incorrect : **{}** [Arg 2]".format(arg2))
            else:
                if not arg3.isdigit() or arg3 is None:
                    await ctx.channel.send("Paramètre manquant / incorrect : **{}** [Arg 3]".format(arg3))
                else:
                    role_obj = get(ctx.guild.roles, name=arg4)
                    db_del_value(arg1, (ctx.guild.id, int(arg2), int(arg3), int(arg4)))
        ##
        elif arg1 in ['add_uwu_admin', 'del_uwu_admin']:
            res = db_check_privilege(ctx.guild.id, ctx.author.id)
            if res is False:  # Check if user is an uwu admin
                await ctx.channel.send("Vous n'avez pas les privilèges nécéssaires pour executer cette commande")
            else:
                member_obj = get(ctx.guild.members, id=int(arg2))
                if member_obj is not None:  # Check if user_id exist
                    if not check_if_owner(ctx.guild, int(arg2)):  # Check if the target is owner
                        if arg3.isdigit() and arg3 is not None and int(arg3) in [2, 3]:  # Arg3 data validation
                            db_insupdel_admin(arg1, ctx.guild.name, ctx.guild.id, member_obj.name, member_obj.id, int(arg3))
                        else:
                            await ctx.channel.send(
                                "Paramètre manquant / incorrect : **{}** [Arg 3] (nombre entier entre 2 et 3 requis)"
                                .format(arg3))
                    else:
                        await ctx.channel.send(
                            "Vous ne pouvez pas modifier le status du propriétaire du serveur ! : **{}** [Arg 2]"
                            .format(arg2))
                else:
                    await ctx.channel.send(
                        "Aucun utilisateur n'a été trouvé sur cet ID : **{}** [Arg 2]"
                        .format(arg2))
        ##
        else:
            await ctx.channel.send(
                "Paramètre manquant / incorrect : **{}** [Arg 1] (l'action sélectionnée n'existe pas)"
                .format(arg1))

    @admin_restricted()
    @commands.command()
    async def shodconfig(self, ctx, arg1: chk_arg1_shcfg):
        if arg1 == 'general':  # GOOD
            # Get infos from DB
            conf_server_all = db_get_conf_server_all(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configurations globales : **__", value="\u200b", inline=False)
            # Change field depending on NSFW mode
            if conf_server_all[0] == 0:
                embed.add_field(name="nsfw_mode",
                                value=' 0\u20e3 : NSFW disabled on the server', inline=False)
            elif conf_server_all[0] == 1:
                embed.add_field(name="nsfw_mode",
                                value=' 1\u20e3 : NSFW allowed on the server, on a per-channel rule',
                                inline=False)
            elif conf_server_all[0] == 2:
                embed.add_field(name="nsfw_mode",
                                value=' 2\u20e3 : NSFW allowed on the server without any restriction',
                                inline=False)
            # Embed
            embed.add_field(name="short_reddit_timer", value=conf_server_all[1], inline=False)
            embed.add_field(name="long_reddit_timer", value=conf_server_all[2], inline=False)
            if conf_server_all[3] is None:
                embed.add_field(name="censor_log_channel", value="❌", inline=False)
            else:
                embed.add_field(name="censor_log_channel", value="<#" + str(conf_server_all[3]) + ">", inline=False)
            if conf_server_all[4] is None:
                embed.add_field(name="welcome_channel", value="❌", inline=False)
            else:
                embed.add_field(name="welcome_channel", value="<#" + str(conf_server_all[4]) + ">", inline=False)
            if conf_server_all[5] is None:
                embed.add_field(name="welcome_role", value="❌", inline=False)
            else:
                embed.add_field(name="welcome_role", value="<@&" + str(conf_server_all[5]) + ">", inline=False)
            if conf_server_all[6] is None:
                embed.add_field(name="approb_role", value="❌", inline=False)
            else:
                embed.add_field(name="approb_role", value="<@&" + str(conf_server_all[6]) + ">", inline=False)
            if conf_server_all[7] is None:
                embed.add_field(name="goulag_channel", value="❌", inline=False)
            else:
                embed.add_field(name="goulag_channel", value="<@&" + str(conf_server_all[7]) + ">", inline=False)
            await ctx.channel.send(embed=embed)
        ##
        elif arg1 == 'censor':  # GOOD
            # Get infos from DB
            censor_words_dict = db_get_censor_words(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration de la censure: **__", value="\u200b", inline=False)
            if not censor_words_dict:  # Check if no values to display
                embed.add_field(name="\u200b", value="Aucune configuration trouvée.", inline=True)
            else:
                # Iterate trough dict
                for k, v in censor_words_dict.items():
                    if v is None:
                        embed.add_field(name=k, value="\u200b", inline=True)
                    else:
                        embed.add_field(name=k, value=v, inline=True)

            await ctx.channel.send(embed=embed)
        ##
        elif arg1 == 'censor_excluded':  # GOOD
            # Get infos from DB
            censor_excl_list = db_get_excl_channels(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration de channels exclus (censure): **__", value="\u200b", inline=False)
            if not censor_excl_list:  # Check if no values to display
                embed.add_field(name="\u200b", value="Aucune configuration trouvée.", inline=True)
            else:
                # List iteration to show all channels
                for e in censor_excl_list:
                    embed.add_field(name="**ID :** " + str(e), value="<#" + str(e) + ">", inline=True)

            await ctx.channel.send(embed=embed)
        ##
        elif arg1 == 'emoji_roles':  # GOOD
            # Get infos from DB
            emoji_roles_list = db_get_server_emoji_roles(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration d'emoji-roles: **__", value="\u200b", inline=False)
            if not emoji_roles_list:
                embed.add_field(name="\u200b", value="Aucune configuration trouvée.", inline=True)
            else:
                # List iteration to show tracked message / emoji / role added
                for e in emoji_roles_list:
                    embed.add_field(name=str(e[2]), value="<:_:" + str(e[0]) + "> | " + "<@&" + str(e[1]) + ">", inline=False)

            await ctx.channel.send(embed=embed)
        ##
        elif arg1 == 'nsfw_channels':  # GOOD
            # Get infos from DB
            nsfw_channel_list = db_get_nsfw_channels(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration des channels NSFW: **__", value="\u200b", inline=False)
            if not nsfw_channel_list:  # Check if no values to display
                embed.add_field(name="\u200b", value="Aucune configuration trouvée.", inline=True)
            else:
                # List iteration to show all channels
                for e in nsfw_channel_list:
                    embed.add_field(name="**ID :** " + str(e), value="<#" + str(e) + ">", inline=True)

            await ctx.channel.send(embed=embed)
        ##
        else:
            await ctx.channel.send(
                "Paramètre manquant / incorrect : **{}** [Arg 1] (l'action sélectionnée n'existe pas)"
                .format(arg1))

    # LOCAL ERROR-HANDLERS ############################################################################
    ###################################################################################################

    @shodconfig.error
    async def shodconfig_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Commande shodconfig 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Syntaxe : **__", value="!shodconfig [configuration]", inline=False)
            embed.add_field(name="general", value="Options de configurations globales du serveur.", inline=False)
            embed.add_field(name="censor", value="Mots bannis et remplacants.", inline=False)
            embed.add_field(name="censor_excluded", value="Channels exclus de la censure textuelle.", inline=False)
            embed.add_field(name="emoji_roles", value="Reactions d'emoji donnant accés à certains rôles.", inline=False)
            embed.add_field(name="nsfw_channels", value="Channels ou les commandes NSFW sont autorisées.", inline=False)
            await ctx.channel.send(embed=embed)

    @sendconfig.error
    async def sendconfig_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
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


def setup(bot):
    bot.add_cog(ConfigMenu(bot))
