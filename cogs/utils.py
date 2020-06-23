import logging
from discord.ext import commands

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] Utils COG loaded')


# Return current guild id from context
def guild_from_context(ctx):
    current_guild = ctx.message.guild.id
    return current_guild


# Check if arg1 in !sendconfig command is correct
def chk_arg1_sndcfg(param):
    parameters_list = ["nsfw_mode", "short_reddit_timer", "long_reddit_timer", "censor_log_channel",
                       "welcome_channel", "welcome_role", "approb_role", "add_nsfw_channel", "add_banned_word",
                       "del_banned_word", "add_censor_excluded_channel", "add_emoji_role", "add_uwu_admin",
                       "del_uwu_admin"]

    if param in parameters_list:
        return param
    else:
        raise commands.BadArgument("Premier paramètre incorrect : '{}'".format(param))


# Check if arg1 in !shodconfig command is correct
def chk_arg1_shcfg(param):
    parameters_list = ["general", "censor", "censor_excluded", "emoji_roles", "nsfw_channels", "moderation"]

    if param in parameters_list:
        return param
    else:
        raise commands.BadArgument("Premier paramètre incorrect : '{}'".format(param))


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

    @commands.command(name='reload', hidden=True)
    async def reload_cog(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot):
    bot.add_cog(Utils(bot))
