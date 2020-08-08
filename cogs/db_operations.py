import sys
import logging
import mysql.connector
from discord.ext import commands
from mysql.connector import Error
from loadconfig import db_host, db_name, db_user, db_pass

# Variable de connection a la DB
connection = mysql.connector.connect(host=db_host, database=db_name, user=db_user, password=db_pass)

# Retrieve logger
log = logging.getLogger("BlackBot_log")

log.info('[COGS] DBOperations COG loaded')


# CHECK-DB #####################################################################################################
################################################################################################################

def db_uwu_check():
    testing_cursor = None
    try:
        if connection.is_connected():
            db_info = connection.get_server_info()
            log.info("Connecté a MYSQL server version " + str(db_info))
            testing_cursor = connection.cursor()
            testing_cursor.execute("select database();")
            record = testing_cursor.fetchone()
            log.info("Connecté a la base de donnée: " + str(record))

    except Error as e:
        log.info("Erreur lors de la connection a MYSQL, fin du programme !" + str(e))
        sys.exit()

    finally:
        if connection.is_connected():
            testing_cursor.close()
            log.info("Fin du test de connection MYSQL")


# Check if server data already exist
def db_check_serv_data(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT guild_id from servers_settings_global WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    cursor.close()
    if result:
        return True
    else:
        return False


# Create server initial data (with their default values)
def db_create_serv_data(guild_name, guild_id):
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO servers_settings_global (guild_name, guild_id) VALUES (%s, %s)''', (guild_name, guild_id))
    connection.commit()
    cursor.close()


# GET GLOBAL CONFS #############################################################################################
################################################################################################################

def db_get_conf_server_all(guild_id):
    connection.commit()
    cursor = connection.cursor()

    cursor.execute('''SELECT nsfw_mode, short_reddit_timer, long_reddit_timer, censor_log_channel, welcome_channel, 
    welcome_role, approb_role, goulag_channel, warn_to_goulag, pmoji_user, pmoji_emoji, pmoji_message 
    from servers_settings_global WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    cursor.close()
    if result:
        return result
    else:
        return None


# GET INFOS FROM DB ############################################################################################
################################################################################################################

def db_get_reddit_command_dict():
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT command_name, sub_name, is_nsfw, submission_nb, sub_group from uwu_reddit_scrap WHERE 
    sub_group = '' ''')
    result = cursor.fetchall()  # Result is a [list] of [tuple]
    cursor.close()
    res = {}
    for i, j, k, l, m in result:
        res[i] = [j, k, l, m]
    return res


def db_get_reddit_sub_dict():
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT sub_name, is_nsfw, submission_nb, sub_group from uwu_reddit_scrap''')
    result = cursor.fetchall()  # Result is a [list] of [tuple]
    cursor.close()
    res = {}
    for i, j, k, l in result:
        res[i] = [j, k, l]
    return res


def db_get_nsfw_channels(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT channel_id from servers_nsfw_channel WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]
    cursor.close()
    query_list = [a_tuple[0] for a_tuple in result]  # Convert [list of tuples] to a [list]
    return query_list


def db_get_censor_words(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT word, word_replacement from servers_banned_word WHERE guild_id = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # # Result is a [list of tuples]
    cursor.close()
    query_dict = dict(result)
    return query_dict


# Get all excluded channels that does not get censored on the server
def db_get_excl_channels(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT channel_id from servers_censor_excluded_channel WHERE guild_id = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]
    cursor.close()
    if result:
        query_list = [a_tuple[0] for a_tuple in result]  # Convert [list of tuples] to a [list]
        return query_list
    else:
        return None


# Get all the emoji-roles on the server matching a specific message
def db_get_emoji_roles(guild_id, message_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT emoji_id, role_id from servers_emoji_roles WHERE guild_id = %s AND tracked_message = %s''',
                   (guild_id, message_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]
    cursor.close()
    if result:
        query_dict = dict(result)
        return query_dict
    else:
        return None


# Get all the emoji-roles on the server
def db_get_server_emoji_roles(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT emoji_id, role_id, tracked_message from servers_emoji_roles WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]
    cursor.close()
    if result:
        return result
    else:
        return None


# Check the privilege of a user that try to input admin commands
def db_check_privilege(guild_id, user_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT privilege_level from servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    cursor.close()
    if result:
        return result[0]
    else:
        return False


def db_get_admins(guild_id):
    pass
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT user_id, privilege_level from servers_global_privileges WHERE guild_id = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # Result is a [list] of [tuples]
    cursor.close()
    if result:
        return result
    else:
        return False


# INSERT/UPDATE/DELETE INFOS TO DB #############################################################################
################################################################################################################

# Insert val_tuple values into DB depending on invoked usage
def db_insup_value(target_param, val_tuple):
    cursor = connection.cursor()
    connection.commit()
    ##
    if target_param == "nsfw_mode":
        guild_id, nsfw_mode = val_tuple
        if nsfw_mode == "reset":
            cursor.execute('''UPDATE servers_settings_global SET nsfw_mode = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET nsfw_mode = %s
                                        WHERE guild_id = %s''', (int(nsfw_mode), guild_id,))
    ##
    elif target_param == "short_reddit_timer":
        guild_id, short_reddit_timer = val_tuple
        if short_reddit_timer == "reset":
            cursor.execute('''UPDATE servers_settings_global SET short_reddit_timer = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET short_reddit_timer = %s 
                                        WHERE guild_id = %s''', (int(short_reddit_timer), guild_id,))
    ##
    elif target_param == "long_reddit_timer":
        guild_id, long_reddit_timer = val_tuple
        if long_reddit_timer == "reset":
            cursor.execute('''UPDATE servers_settings_global SET long_reddit_timer = DEFAULT 
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET long_reddit_timer = %s 
                                        WHERE guild_id = %s''', (int(long_reddit_timer), guild_id,))
    ##
    elif target_param == "censor_log_channel":
        guild_id, censor_log_channel = val_tuple
        if censor_log_channel == "reset":
            cursor.execute('''UPDATE servers_settings_global SET censor_log_channel = DEFAULT 
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET censor_log_channel = %s 
                                        WHERE guild_id = %s''', (censor_log_channel, guild_id,))
    ##
    elif target_param == "welcome_channel":
        guild_id, welcome_channel = val_tuple
        if welcome_channel == "reset":
            cursor.execute('''UPDATE servers_settings_global SET welcome_channel = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET welcome_channel = %s 
                                        WHERE guild_id = %s''', (welcome_channel, guild_id,))
    ##
    elif target_param == "welcome_role":
        guild_id, welcome_role = val_tuple
        if welcome_role == "reset":
            cursor.execute('''UPDATE servers_settings_global SET welcome_role = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET welcome_role = %s 
                                        WHERE guild_id = %s''', (welcome_role, guild_id,))
    ##
    elif target_param == "approb_role":
        guild_id, approb_role = val_tuple
        if approb_role == "reset":
            cursor.execute('''UPDATE servers_settings_global SET approb_role = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
        else:
            cursor.execute('''UPDATE servers_settings_global SET approb_role = %s 
                                        WHERE guild_id = %s''', (approb_role, guild_id,))
    ##
    elif target_param == "add_nsfw_channel":
        guild_id, guild_name, channel_id, channel_name = val_tuple
        cursor.execute('''SELECT channel_name from servers_nsfw_channel WHERE guild_id = %s and channel_id = %s''',
                       (guild_id, channel_id,))
        result = cursor.fetchone()
        if result:
            return False
        else:
            cursor.execute('''INSERT INTO servers_nsfw_channel (guild_id, guild_name, channel_id, channel_name) 
                                      VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, channel_id, channel_name,))
    ##
    elif target_param == "add_censor_excluded_channel":
        guild_id, guild_name, channel_id, channel_name = val_tuple
        cursor.execute('''SELECT channel_name from servers_censor_excluded_channel WHERE guild_id = %s
                        and channel_id = %s''', (guild_id, channel_id,))
        result = cursor.fetchone()
        if result:
            return False
        else:
            cursor.execute('''INSERT INTO servers_censor_excluded_channel (guild_id, guild_name, channel_id, 
                            channel_name) VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, channel_id, channel_name,))
    ##
    elif target_param == "add_banned_word":
        guild_id, guild_name, word, word_replacement = val_tuple
        cursor.execute('''SELECT word from servers_banned_word WHERE guild_id = %s and word = %s''',
                       (guild_id, word,))
        result = cursor.fetchone()
        if result:
            cursor.execute('''UPDATE servers_banned_word SET word_replacement = %s 
            WHERE guild_id = %s and word = %s''', (word_replacement, guild_id, word,))
        else:
            cursor.execute('''INSERT INTO servers_banned_word (guild_id, guild_name, word, word_replacement) 
                              VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, word, word_replacement,))
    ##
    elif target_param == "add_emoji_role":
        guild_id, guild_name, role_name, tracked_message, emoji_id, role_id = val_tuple
        cursor.execute('''SELECT emoji_id from servers_emoji_roles WHERE guild_id = %s and emoji_id = %s''',
                       (guild_id, emoji_id,))
        result = cursor.fetchone()
        if result:
            return False
        else:
            cursor.execute('''INSERT INTO servers_emoji_roles 
                          (guild_id, guild_name, role_name, tracked_message, emoji_id, role_id) 
            VALUES (%s, %s, %s, %s, %s, %s)''', (guild_id, guild_name, role_name, tracked_message, emoji_id, role_id,))

    connection.commit()
    cursor.close()


# Delete val_tuple values from DB depending on invoked usage
def db_del_value(target_param, val_tuple):
    cursor = connection.cursor()
    connection.commit()
    ##
    if target_param == 'del_nsfw_channel':
        guild_id, channel_id = val_tuple
        cursor.execute('''DELETE FROM servers_nsfw_channel WHERE guild_id = %s and channel_id = %s''',
                       (guild_id, channel_id,))
    ##
    elif target_param == 'del_censor_excluded_channel':
        guild_id, channel_id = val_tuple
        cursor.execute('''DELETE FROM servers_censor_excluded_channel WHERE guild_id = %s and channel_id = %s''',
                       (guild_id, channel_id,))
    ##
    elif target_param == 'del_banned_word':
        guild_id, word = val_tuple
        cursor.execute('''SELECT word from servers_banned_word WHERE guild_id = %s and word = %s''',
                       (guild_id, word,))
        result = cursor.fetchone()
        if result:
            cursor.execute('''DELETE FROM servers_banned_word WHERE guild_id = %s and word = %s''', (guild_id, word,))
        else:
            return False
    ##
    elif target_param == 'del_emoji_role':
        guild_id, tracked_message, emoji_id, role_id = val_tuple
        cursor.execute('''SELECT emoji_id from servers_emoji_roles WHERE guild_id = %s and emoji_id = %s''',
                       (guild_id, emoji_id,))
        result = cursor.fetchone()
        if result:
            cursor.execute('''DELETE FROM servers_emoji_roles WHERE guild_id = %s and tracked_message =%s 
                              and emoji_id = %s and  role_id = %s''', (guild_id, tracked_message, emoji_id, role_id,))
        else:
            return False

    connection.commit()
    cursor.close()


# Check if owner-admin exist, and if not, create it
def db_inspass_admin(guild_name, guild_id, user_name, user_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT user_id from servers_global_privileges WHERE guild_id = %s and user_id = %s 
                    and privilege_level = 2''', (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    if result:
        pass
    else:
        cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, privilege_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 2,))
    connection.commit()
    cursor.close()


# Insert / Update / Delete an admin from the DB
def db_insupdel_admin(target_param, guild_name, guild_id, user_name, user_id):
    cursor = connection.cursor()
    connection.commit()
    cursor.execute('''SELECT privilege_level FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    if target_param == 'add_uwu_admin':
        if result[0] == 1:
            return True
        if result[0] == 2:
            return False
        elif result[0] == 3:
            cursor.execute('''UPDATE servers_global_privileges SET privilege_level = %s 
                            WHERE guild_id = %s and user_id = %s''', (2, guild_id, user_id,))
        else:
            cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, 
            privilege_level) VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 2,))

    elif target_param == 'del_uwu_admin':
        if result[0] == 1:
            return True
        if result[0] == 2:
            cursor.execute('''DELETE FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                           (guild_id, user_id,))
        elif result[0] == 3:
            return False
        else:
            return False

    connection.commit()
    cursor.close()


# Insert / Update / Delete an mod from the DB
def db_insupdel_mod(target_param, guild_name, guild_id, user_name, user_id):
    cursor = connection.cursor()
    connection.commit()
    cursor.execute('''SELECT privilege_level FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    if target_param == 'add_uwu_mod':
        if result[0] == 1:
            return True
        if result[0] == 3:
            return False
        elif result[0] == 2:
            cursor.execute('''UPDATE servers_global_privileges SET privilege_level = %s 
                            WHERE guild_id = %s and user_id = %s''', (3, guild_id, user_id,))
        else:
            cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, 
            privilege_level) VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 3,))

    elif target_param == 'del_uwu_mod':
        if result[0] == 1:
            return True
        if result[0] == 3:
            cursor.execute('''DELETE FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                           (guild_id, user_id,))
        elif result[0] == 2:
            return False
        else:
            return False

    connection.commit()
    cursor.close()


# Add the precusor as level-1 on the server
def db_inspass_precursor(guild_name, guild_id, dev_name, dev_id):
    cursor = connection.cursor()
    connection.commit()
    cursor.execute('''SELECT user_id from servers_global_privileges WHERE guild_id = %s and user_id = %s 
                        and privilege_level = 1''', (guild_id, dev_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    if result:
        pass
    else:
        cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, privilege_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, dev_name, dev_id, 1,))
    connection.commit()
    cursor.close()


# Add a warn to a user, create it if not already in DB
def db_add_warn(guild_name, guild_id, user_name, user_id, warn_level):
    cursor = connection.cursor()
    connection.commit()
    cursor.execute('''SELECT user_id FROM servers_moderation_data WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Return is a [tuple]

    if result:
        cursor.execute('''UPDATE servers_moderation_data SET warn_level = warn_level + %s
                        WHERE guild_id = %s and user_id = %s''', (warn_level, guild_id, user_id,))
    else:
        cursor.execute('''INSERT INTO servers_moderation_data (guild_name, guild_id, user_name, user_id, warn_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, warn_level,))

    connection.commit()
    cursor.close()


class DBOperations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(DBOperations(bot))
