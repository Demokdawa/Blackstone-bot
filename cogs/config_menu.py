import discord
from discord.ext import tasks, commands
from discord.utils import get
import logging
from cogs.utils import chk_arg1_prm, check_if_owner
from cogs.db_operations import db_insup_value, db_check_privilege, db_insdel_admin

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] ConfigMenu COG loaded')


class ConfigMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command that call db insert/update function to modify/add configs to the DB
    # Arg1 = param name, Arg2 = Value of config, Arg* = Others values of config
    @commands.command()
    async def sendconfig(self, ctx, arg1: chk_arg1_prm, arg2=None, arg3=None, arg4=None):

        if arg1 == 'nsfw_mode':  # GOOD
            print('yes')
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
        # Reduce size of the line using a list instead
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
            elif res in [1, 2]:  # Check privileges
                member_obj = get(ctx.guild.members, id=int(arg2))
                if member_obj is not None:  # Check if user_id exist
                    if not check_if_owner(ctx.guild, int(arg2)):  # Check if the target is owner
                        if arg3.isdigit() and arg3 is not None and int(arg3) in [2, 3]:  # Arg3 data validation
                            db_insdel_admin(arg1, ctx.guild.name, ctx.guild.id, member_obj.name, member_obj.id, int(arg3))
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
                        "Cet utilisateur n'existe pas ou n'est pas correctement renseigné : **{}** [Arg 2]"
                        .format(arg2))
            else:
                await ctx.channel.send("Vous n'avez pas les privilèges nécéssaires pour executer cette commande")
        ##
        else:
            await ctx.channel.send(
                "Paramètre manquant / incorrect : **{}** [Arg 1] (l'action sélectionnée n'existe pas"
                .format(arg1))


def setup(bot):
    bot.add_cog(ConfigMenu(bot))
