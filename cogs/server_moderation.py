import logging
from discord.ext import commands
from discord.utils import get
from cogs.db_operations import db_get_emoji_roles, db_get_conf_server_all

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] Moderation COG loaded')


# DECORATORS #####################################################################################
##################################################################################################

# Decorator to check if server_moderation is configured on this server
def check_cog_censor_config():
    def predicate(ctx):
        conf_server_all = db_get_conf_server_all(ctx.guild.id)
        error_nbr = 0
        if conf_server_all is None:
            raise commands.UserInputError("Ce serveur n\'est pas configuré pour utiliser cette commande !")
        else:
            if conf_server_all[4] is None:
                error_nbr += 1
            if conf_server_all[5] is None:
                error_nbr += 1
            if conf_server_all[6] is None:
                error_nbr += 1

            if error_nbr == 0:
                return True
            else:
                raise commands.UserInputError("Ce serveur n\'est pas configuré pour utiliser cette commande !/n"
                                              "Configurations erronées/manquantes : {}/n"
                                              "Utilise la commande configuration pour voir ce qui ne va pas !"
                                              .format(error_nbr))

    return commands.check(predicate)


class ServerModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def moderation_react_process(self, payload, action):

        # Variables needed to operate
        emoji_roles_list_dict = db_get_emoji_roles(payload.guild_id, payload.message_id)  # Get emoji/roles links from DB
        linked_role = emoji_roles_list_dict.get(payload.emoji.id)  # Get the role linked to the trigger emoji
        guild = self.bot.get_guild(payload.guild_id)  # Get guild object from the payload
        member = guild.get_member(payload.user_id)  # Get member object from the payload
        conf_server_all = db_get_conf_server_all(payload.guild_id)  # Get global conf values for the server from DB
        silencieux = get(guild.roles, id=conf_server_all[5])  # Get "silencieux" role object
        new_member = get(guild.roles, id=conf_server_all[6])  # Get "new member" role object
        welcome_channel = self.bot.get_channel(conf_server_all[4])  # Get "welcome" channel object
        list_of_user_roles = [e.id for e in member.roles]  # Get all roles of the user

        if emoji_roles_list_dict is None:  # Check if server have emoji-roles
            return False, None, None, None, None, None, None, None
        else:
            if action == 'add':
                if emoji_roles_list_dict is None:  # Check if server have emoji/roles
                    return False, None, None, None, None, None, None, None
                else:
                    if payload.emoji.id in emoji_roles_list_dict:  # Check if the emoji is linked to a role
                        if conf_server_all[6] in list_of_user_roles:  # Check if user is a "new member"
                            return True, "case1", member, guild, linked_role, silencieux, new_member, welcome_channel
                        else:  # If user does not have "new member" role
                            return True, "case2", member, guild, linked_role, silencieux, new_member, welcome_channel
                    else:
                        return False, None, None, None, None, None, None, None

            if action == 'remove':
                if payload.emoji.id in emoji_roles_list_dict:
                    return True, member, guild, linked_role
                else:
                    return False, None, None, None

    # NEW-MEMBERS AND MEMBERS ROLE ATTRIB ############################################################
    ##################################################################################################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        res, case, member, guild, linked_role, silencieux, new_member, welcome_channel = self.moderation_react_process(payload, action="add")

        if res is False:  # Check if server have emoji-roles
            print("Emoji ne correspond a rien, aucune action !")
        if res is True:
            if case == "case1":
                await member.add_roles(get(guild.roles, id=linked_role), silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await welcome_channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif case == "case2":
                await member.add_roles(get(guild.roles, id=linked_role), reason=None, atomic=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        # True/False, member, guild, role_id
        res, member, guild, linked_role = self.moderation_react_process(payload, action="remove")

        if res is True:
            await member.remove_roles(get(guild.roles, id=linked_role), reason=None, atomic=True)
        else:
            print("Emoji ne correspond a rien, aucune action !")


def setup(bot):
    bot.add_cog(ServerModeration(bot))


# For the server_moderation COG : ##
# Need a command to be able to config this
