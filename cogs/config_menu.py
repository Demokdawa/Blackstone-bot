import discord
from discord.ext import tasks, commands
from discord.utils import get
import logging
from cogs.utils import chk_arg1_prm, check_channel_id
from cogs.db_operations import db_insup_value

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

        if arg1 == 'nsfw_mode':  #GOOD
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
        elif arg1 == 'short_reddit_timer':  #GOOD
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
        elif arg1 == 'long_reddit_timer':  #GOOD
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
        elif arg1 in ['censor_log_channel', 'welcome_channel']:  #GOOD
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
        elif arg1 == 'add_banned_word':  #GOOD
            db_insup_value(arg1, (ctx.guild.id, ctx.guild.name, arg2, arg3))
        ##
        elif arg1 == 'del_banned_word':  #GOOD
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
        else:
            await ctx.channel.send(
                "Paramètre manquant / incorrect : **{}** [Arg 1] (l'action sélectionnée n'existe pas"
                .format(arg1))


def setup(bot):
    bot.add_cog(ConfigMenu(bot))
