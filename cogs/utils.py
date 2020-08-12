import logging
from discord.ext import commands
from cogs.db_operations import db_check_privilege

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] Utils COG loaded')


# DECORATORS #####################################################################################
##################################################################################################

# Decorator to check for precursor-only commands
def precursor_restricted():
    async def predicate(ctx):
        res = db_check_privilege(ctx.guild.id, ctx.author.id)
        if res is False or res != 1:
            await ctx.channel.send("Vous n'êtes pas qualifié pour executer cette commande !")
        else:
            return True
    return commands.check(predicate)


# Decorator to check for admin-only commands
def admin_restricted():
    async def predicate(ctx):
        res = db_check_privilege(ctx.guild.id, ctx.author.id)
        if res is False or res not in [1, 2]:
            await ctx.channel.send("Vous n'êtes pas qualifié pour executer cette commande !")
        else:
            return True
    return commands.check(predicate)


# Decorator to check for moderation-only commands
def mod_restricted():
    async def predicate(ctx):
        res = db_check_privilege(ctx.guild.id, ctx.author.id)
        if res is False:
            await ctx.channel.send("Vous n'êtes pas qualifié pour executer cette commande !")
        else:
            return True
    return commands.check(predicate)


# Check if arg1 in !sendconfig command is correct
def chk_arg1_sndcfg(param):
    parameters_list = ["nsfw_mode", "short_reddit_timer", "long_reddit_timer", "censor_log_channel",
                       "welcome_channel", "welcome_role", "approb_role", "add_nsfw_channel", "add_banned_word",
                       "del_nsfw_channel", "del_censor_excluded_channel", "del_banned_word",
                       "add_censor_excluded_channel", "add_emoji_role", "del_emoji_role", "add_uwu_admin",
                       "del_uwu_admin", "add_uwu_mod", "del_uwu_mod", "pmoji_user"]

    if param in parameters_list:
        return param
    else:
        raise commands.BadArgument(
            "Paramètre manquant / incorrect : **{}** [Arg 1] (l'action sélectionnée n'existe pas)".format(param))


# Check if arg1 in !shodconfig command is correct
def chk_arg1_shcfg(param):
    parameters_list = ["general", "censor", "censor_excluded", "emoji_roles", "nsfw_channels"]

    if param in parameters_list:
        return param
    else:
        raise commands.BadArgument(
            "Paramètre manquant / incorrect : **{}** [Arg 1] (l'action sélectionnée n'existe pas)".format(param))


# Take guild object and user_id as args
# Check specified user_id is the owner of the guild
def check_if_owner(guild, user_id):
    if user_id == guild.owner.id:
        return True
    else:
        return False


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @precursor_restricted()
    @commands.command(name='reload', hidden=True)
    async def reload_cog(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @precursor_restricted()
    @commands.command(name='rename_bot', hidden=True)
    async def rename(self, ctx, name: str):
        await self.bot.user.edit(username=name)

    #@precursor_restricted()
    #@commands.command(name='change_bot', hidden=True)
    #async def rename(self, ctx, name: str):
    #    with open('leo.png', 'rb') as f:
    #        await self.bot.user.edit(avatar=f.read())


def setup(bot):
    bot.add_cog(Utils(bot))
