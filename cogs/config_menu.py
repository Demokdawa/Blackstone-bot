import discord
from discord.ext import tasks, commands
from discord.utils import get
import logging
from itertools import zip_longest
from cogs.utils import chk_arg1_sndcfg, chk_arg1_shcfg, check_if_owner
from cogs.db_operations import db_insup_value, db_check_privilege, db_insupdel_admin, db_get_conf_server_all, \
    db_get_censor_words, db_get_excl_channels, db_get_server_emoji_roles, db_get_nsfw_channels

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] ConfigMenu COG loaded')


# DECORATORS #####################################################################################
##################################################################################################

# Decorator to check for admin-only commands
def admin_restricted():
    def predicate(ctx):
        res = db_check_privilege(ctx.guild.id, ctx.author.id)
        if res is False or res not in [1, 2]:
            raise commands.UserInputError("Vous n'êtes pas qualifié pour executer cette commande !")
        else:
            return True
    return commands.check(predicate)


class ConfigMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command that call db insert/update function to modify/add configs to the DB
    # Arg1 = param name, Arg2 = Value of config, Arg* = Others values of config
    @admin_restricted()
    @commands.command()
    async def sendconfig(self, ctx, arg1: chk_arg1_sndcfg, arg2=None, arg3=None, arg4=None):

        if arg1 == 'nsfw_mode':  # GOOD
            if arg2.isdigit() and arg2 is not None:
                if not 0 <= int(arg2) <= 2:
                    await ctx.channel.send(
                        "`Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 0 et 2 requis)`"
                        .format(arg2))
                else:
                    success = db_insup_value(arg1, (ctx.guild.id, int(arg2)))
                    if success is True:
                        await ctx.channel.send('**`SUCCESS`**')
                    else:
                        await ctx.channel.send('**`ERROR`**')
            else:
                await ctx.channel.send(
                    "`Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 0 et 2 requis)`"
                    .format(arg2))
        ##
        elif arg1 == 'short_reddit_timer':  # GOOD
            if arg2.isdigit() and arg2 is not None:
                if not 4 <= int(arg2) <= 30:
                    await ctx.channel.send(
                        "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 4 et 30 requis)"
                        .format(arg2))
                else:
                    success = db_insup_value(arg1, (ctx.guild.id, int(arg2)))
                    if success is True:
                        await ctx.channel.send('**`SUCCESS`**')
                    else:
                        await ctx.channel.send('**`ERROR`**')
            else:
                await ctx.channel.send(
                    "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 4 et 30 requis)"
                    .format(arg2))
        ##
        elif arg1 == 'long_reddit_timer':  # GOOD
            if arg2.isdigit() and arg2 is not None:
                if not 10 <= int(arg2) <= 90:
                    await ctx.channel.send(
                        "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 10 et 90 requis)"
                        .format(arg2))
                else:
                    success = db_insup_value(arg1, (ctx.guild.id, int(arg2)))
                    if success is True:
                        await ctx.channel.send('**`SUCCESS`**')
                    else:
                        await ctx.channel.send('**`ERROR`**')
            else:
                await ctx.channel.send(
                    "Paramètre manquant / incorrect : **{}** [Arg 2] (nombre entre 10 et 90 requis)"
                    .format(arg2))
        ##
        elif arg1 in ['censor_log_channel', 'welcome_channel']:  # GOOD
            channel_obj = get(ctx.guild.channels, name=arg2)
            if channel_obj is None:
                await ctx.channel.send(
                    "Ce channel n'existe pas ou n'est pas correctement renseigné : **{}** [Arg 2]"
                    .format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, channel_obj.id))
        ##
        elif arg1 in ['add_nsfw_channel', 'add_censor_excluded_channel']:
            channel_obj = get(ctx.guild.channels, name=arg2)
            if channel_obj is None:
                await ctx.channel.send(
                    "Ce channel n'existe pas ou n'est pas correctement renseigné : **{}** [Arg 2]"
                    .format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, ctx.guild.name, channel_obj.id))
        ##
        elif arg1 == 'welcome_role' or arg1 == 'approb_role':
            role_obj = get(ctx.guild.roles, name=arg2)
            if role_obj is None:
                await ctx.channel.send(
                    "Ce rôle n'existe pas ou n'est pas correctement renseigné : **{}** [Arg 2]"
                    .format(arg2))
            else:
                db_insup_value(arg1, (ctx.guild.id, role_obj.id))
        ##
        elif arg1 == 'add_banned_word':  # GOOD
            db_insup_value(arg1, (ctx.guild.id, ctx.guild.name, arg2, arg3))
        ##
        elif arg1 == 'del_banned_word':  # GOOD
            db_insup_value(arg1, (ctx.guild.id, arg2))
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
        if arg1 == 'general':  # A FINIR/ CHECKER
            # Get infos from DB
            conf_server_all = db_get_conf_server_all(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configurations globales : **__", value="\u200b", inline=False)
            embed.add_field(name="nsfw_mode", value=conf_server_all[0], inline=False)
            embed.add_field(name="short_reddit_timer", value=conf_server_all[1], inline=False)
            embed.add_field(name="long_reddit_timer", value=conf_server_all[2], inline=False)
            embed.add_field(name="censor_log_channel", value=conf_server_all[3], inline=False)
            embed.add_field(name="welcome_channel", value=conf_server_all[4], inline=False)
            embed.add_field(name="welcome_role", value=conf_server_all[5], inline=False)
            embed.add_field(name="approb_role", value=conf_server_all[6], inline=False)
            embed.add_field(name="goulag_channel", value=conf_server_all[7], inline=False)
            await ctx.channel.send(embed=embed)
        ##
        if arg1 == 'censor':  # A FINIR/ CHECKER
            # Get infos from DB
            censor_words_dict = db_get_censor_words(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration de la censure: **__", value="\u200b", inline=False)
            # Iterate trough dict
            for k, v in censor_words_dict.items():
                if v is None:
                    embed.add_field(name=k, value="\u200b", inline=False)
                else:
                    embed.add_field(name=k, value=v, inline=False)

            await ctx.channel.send(embed=embed)
        ##
        if arg1 == 'censor_excluded':  # A FINIR/ CHECKER
            # Get infos from DB
            censor_excl_list = db_get_excl_channels(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration de channels exclus (censure): **__", value="\u200b", inline=False)
            # List iteration + manipulation to get pairs to show on menu
            for a, b in zip_longest(censor_excl_list[::2], censor_excl_list[1::2]):  # List format to get 1/2 pairs
                if b is not None:
                    embed.add_field(name="<#" + str(a[0]) + ">", value="<#" + str(b[0]) + ">", inline=True)
                else:
                    embed.add_field(name="<#" + str(a[0]) + ">", value='\u200b', inline=True)

            await ctx.channel.send(embed=embed)
        ##
        if arg1 == 'emoji_roles':  # A FINIR/ CHECKER
            # Get infos from DB
            emoji_roles_list = db_get_server_emoji_roles(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration d'emoji-roles: **__", value="\u200b", inline=False)
            # Iterate trough list (NEED TO ADD A NONE CHECK)
            for e in emoji_roles_list:
                embed.add_field(name=f"<@" + str(e[0]) + "> | " + "<@&" + str(e[1]) + ">", value=str(e[2]), inline=True)

            await ctx.channel.send(embed=embed)
        ##
        if arg1 == 'nsfw_channels':  # A FINIR/ CHECKER
            # Get infos from DB
            nsfw_channel_list = db_get_nsfw_channels(ctx.guild.id)
            # Create embed
            embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Configuration des channels NSFW: **__", value="\u200b", inline=False)
            #
            for a, b in zip_longest(nsfw_channel_list[::2], nsfw_channel_list[1::2]):  # List format to get 1/2 pairs
                if b is not None:
                    embed.add_field(name=f"<#" + str(a) + ">", value=f"<#" + str(b) + ">", inline=True)
                else:
                    embed.add_field(name=f"<#" + str(a) + ">", value='\u200b', inline=True)
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


def setup(bot):
    bot.add_cog(ConfigMenu(bot))
