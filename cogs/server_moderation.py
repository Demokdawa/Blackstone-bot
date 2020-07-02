import logging
import discord
from discord.ext import commands
from discord.utils import get
from cogs.db_operations import db_get_emoji_roles, db_get_conf_server_all, db_check_privilege, db_add_warn, \
    db_get_admins

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] Moderation COG loaded')

# DECORATORS #####################################################################################
##################################################################################################


# Decorator to check if server_moderation is configured on this server
def check_cog_mod_config():
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


# Decorator to check for moderation-only commands
def mod_restricted():
    def predicate(ctx):
        res = db_check_privilege(ctx.guild.id, ctx.author.id)
        if res is False:
            raise commands.UserInputError("Vous n'êtes pas qualifié pour executer cette commande !")
        else:
            return True
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
        moji_member = None

        if emoji_roles_list_dict is None:  # Check if server have emoji-roles
            return False, None, None, None, None, None, None, None, None

        else:
            if action == 'add':
                # Check if the message and the emoji are the right ones for pmoji
                if conf_server_all[9] is not None and int(conf_server_all[11]) == payload.message_id \
                        and int(conf_server_all[10]) == payload.emoji.id:
                    moji_member = get(guild.members, id=int(conf_server_all[9]))
                    if moji_member is not None:
                        return True, "case_moji_clan", member, guild, linked_role, silencieux, new_member, welcome_channel, \
                               moji_member
                    else:
                        pass

                if payload.emoji.id in emoji_roles_list_dict:  # Check if the emoji is linked to a role
                    if conf_server_all[6] in list_of_user_roles:  # Check if user is a "new member"
                        return True, "case_new_member", member, guild, linked_role, silencieux, new_member, welcome_channel, \
                               moji_member
                    else:  # If user does not have "new member" role
                        return True, "case_member", member, guild, linked_role, silencieux, new_member, welcome_channel, \
                               moji_member
                else:
                    return False, None, None, None, None, None, None, None, None

            if action == 'remove':
                if payload.emoji.id in emoji_roles_list_dict:
                    return True, member, guild, linked_role
                else:
                    return False, None, None, None

    # NEW-MEMBERS AND MEMBERS ROLE ATTRIB ############################################################
    ##################################################################################################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        res, case, member, guild, linked_role, silencieux, new_member, welcome_channel, moji_member \
            = self.moderation_react_process(payload, action="add")

        if res is False:  # Check if server have emoji-roles
            pass
        if res is True:
            if case == "case_new_member":
                await member.add_roles(get(guild.roles, id=linked_role), silencieux, reason=None, atomic=True)
                await member.remove_roles(new_member, reason=None, atomic=True)
                await welcome_channel.send('Ey les amis, souhaitez tous la bienvenue a ' + member.name + ' parmis nous !')
            elif case == "case_member":
                await member.add_roles(get(guild.roles, id=linked_role), reason=None, atomic=True)
            elif case == "case_moji_clan":
                await moji_member.send("Cet utilisateur a demandé a rejoindre le clan Warframe : **{}**"
                                       .format(member.name))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        # True/False, member, guild, role_id
        res, member, guild, linked_role = self.moderation_react_process(payload, action="remove")

        if res is True:
            await member.remove_roles(get(guild.roles, id=linked_role), reason=None, atomic=True)
        else:
            print("Emoji ne correspond a rien, aucune action !")

    # MODERATION COMMANDS ############################################################################
    ##################################################################################################

    @mod_restricted()
    @commands.command()
    async def sendwarn(self, ctx, user: discord.User, arg2: int, arg3='X'):
        if 1 <= int(arg2) <= 4:
            db_add_warn(ctx.guild.name, ctx.guild.id, user.name, user.id, arg2)

            embed = discord.Embed()
            embed.set_author(name="[WARN] " + str(user.display_name), icon_url=user.avatar_url)
            embed.add_field(name="User", value="<@" + str(user.id) + ">", inline=True)
            embed.add_field(name="Moderator", value="<@" + str(ctx.author.id) + ">", inline=True)
            embed.add_field(name="Reason", value=arg3, inline=True)
            embed.add_field(name="Warn-Level", value=str(arg2), inline=False)

            # Get censor log configured channel for the guild from DB
            channel = self.bot.get_channel(db_get_conf_server_all(ctx.guild.id)[3])
            await channel.send(embed=embed)

        else:
            await ctx.channel.send(
                "Valeur incorrecte : **{}** [Arg 2] (nombre entier entre 1 et 4 requis)"
                .format(arg2))

    @mod_restricted()
    @commands.command()
    async def shodadmin(self, ctx):
        # Get infos from DB
        admin_list = db_get_admins(ctx.guild.id)
        # Create embed
        embed = discord.Embed(title="Configuration du Bot 🤖", description="", color=0xd5d500)
        embed.add_field(name="__**Liste des droits : **__", value="\u200b", inline=False)

        for e in admin_list:
            if e[1] == 1:
                embed.add_field(name="\u200b", value="<@" + str(e[0]) + "> | Precurseur", inline=False)
            if e[1] == 2:
                embed.add_field(name="\u200b", value="<@" + str(e[0]) + "> | Admin", inline=False)
            if e[1] == 3:
                embed.add_field(name="\u200b", value="<@" + str(e[0]) + "> | Moderateur", inline=False)

        await ctx.channel.send(embed=embed)

    # LOCAL ERROR-HANDLERS ############################################################################
    ###################################################################################################

    @sendwarn.error
    async def sendwarn_error(self, ctx, error):
        argument = list(ctx.command.clean_params)[len(ctx.args[2:] if ctx.command.cog else ctx.args[1:])]
        print(argument)
        # NEED TO USE ARGUMENT VAR TO DIFFERENTIATE MESSAGES DEPENDING ON CONVERTERS THAT FAILS
        if isinstance(error, commands.BadArgument):
            await ctx.send('Je n\'ai pas pu trouver ce membre, desolé !')
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Commande sendwarn 🤖", description="", color=0xd5d500)
            embed.add_field(name="__**Syntaxe : **__", value="!sendwarn [mention] [warning-level] [raison]", inline=False)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerModeration(bot))


# For the server_moderation COG : ##
# Need a command to be able to config this
