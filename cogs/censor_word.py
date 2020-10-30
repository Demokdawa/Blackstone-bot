import logging
import discord
from discord.ext import commands
from cogs.db_operations import db_get_censor_words, db_get_excl_channels, db_get_conf_server_all

# Retrieve logger
log = logging.getLogger("General_logs")

log.info('[COGS] CensorWord COG loaded')

# FUNCTIONS ######################################################################################
##################################################################################################


def censor_message(message):

    censor_words_dict = db_get_censor_words(message.guild.id)        # [dict] of words banned on the guild
    curse_words_nbr = 0                                              # Number of curse words detected
    censored_message = '**' + message.author.display_name + '** : '  # Discord-formatting for the final message
    censor_char = "*"                                                # Censor character if no replacement word is set

    replaced = None

    for i in message.content.split(' '):
        for k, v in censor_words_dict.items():
            replaced = False
            if k.casefold() == i.casefold():
                replaced = True
                curse_words_nbr += 1
                if v is None:
                    censored_message += f"{discord.utils.escape_markdown(censor_char * len(i))} "
                else:
                    censored_message += f"{v} "
                break
            else:
                pass
        if not replaced:
            censored_message += f"{i} "

    if curse_words_nbr > 0:
        return censored_message  # Return string containing corrected message
    else:
        return None


def check_message_context(message):

    # Check if the messae is not sent by a bot xD
    if message.author.bot:
        return None
    else:
        # Get censor exclude [list] of channels from DB
        censor_excl_list = db_get_excl_channels(message.guild.id)

        if censor_excl_list is None:  # If there is no channels excluded for the guild"

            # Check if word is banned from the server
            censored_message = censor_message(message)

            if censored_message is None:  # If there is no banned words...
                return None  # Do nothing and let the message pass the filter
            else:
                return censored_message

        else:
            if message.channel.id in censor_excl_list:
                return None  # Do nothing and let the message pass the filter
            else:
                # Check if word is banned from the server
                censored_message = censor_message(message)

                if censored_message is None:  # If there is no banned words...
                    return None  # Do nothing and let the message pass the filter
                else:
                    return censored_message

# DECORATORS #####################################################################################
##################################################################################################


# !! UNUSED FOR NOW !! ###############
# Decorator to check if CensorWord is configured on this server
def check_cog_censor():
    async def predicate(ctx):
        conf_server_all = db_get_conf_server_all(ctx.guild.id)
        if conf_server_all is None:
            await ctx.channel.send("Ce serveur n\'est pas configuré pour utiliser cette commande !")
        else:
            if conf_server_all[3] is None:
                await ctx.channel.send("Ce serveur n\'est pas configuré pour utiliser cette commande !/n"
                                       "Utilise la commande configuration pour voir ce qui ne va pas !")

    return commands.check(predicate)

# !! UNUSED FOR NOW !! ###############


class CensorWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # EVENTS #########################################################################################
    ##################################################################################################

    # Censoring function
    @commands.Cog.listener()
    async def on_message(self, message):

        # Get ctx and check if message is a command
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            pass
        else:
            # Check message and context for censoring
            message_censored = check_message_context(message)

            if message_censored is None:
                pass  # Do nothing and let the message pass the filter
            else:
                embed = discord.Embed()
                embed.set_author(name="[CORRECT] " + str(message.author.display_name), icon_url=message.author.avatar_url)
                embed.add_field(name="User", value="<@" + str(message.author.id) + ">", inline=True)
                embed.add_field(name="Reason", value="Bad word usage", inline=True)
                embed.add_field(name="Channel", value="<#" + str(message.channel.id) + ">", inline=False)
                embed.add_field(name="Message", value=str(message.content), inline=False)

                # Get censor log configured channel for the guild from DB
                channel = self.bot.get_channel(db_get_conf_server_all(message.guild.id)[3])

                # print(dict(message.channel.permissions_for(ctx.me)))

                await channel.send(embed=embed)
                await message.delete()
                await message.channel.send(message_censored)


def setup(bot):
    bot.add_cog(CensorWord(bot))

# For the censor_word COG : ##
