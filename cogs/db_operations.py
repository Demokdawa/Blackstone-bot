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


# CHECK-DB #######################################################################################
##################################################################################################

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


# GET GLOBAL CONFS ###############################################################################
##################################################################################################

def db_get_conf_server_all(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT nsfw_mode, short_reddit_timer, long_reddit_timer, censor_log_channel, welcome_channel, 
    welcome_role, approb_role, goulag_channel from servers_settings_global WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    cursor.close()
    if result:
        return result
    else:
        return None


def db_get_conf_welcome_channel(guild_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT welcome_channel from servers_emoji_roles WHERE guild_id = %s AND tracked_message = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]
    cursor.close()
    if result:
        query_dict = dict(result)
        return query_dict
    else:
        return None


# GET INFOS FROM DB ##############################################################################
##################################################################################################

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


# Check the privilege of a user that try to input admin commands
def db_check_privilege(guild_id, user_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT privilege_level from uwu_global_admins WHERE guild_id = %s AND user_id = %s ''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    cursor.close()
    if result:
        return result[0]
    else:
        return False


# INSERT/UPDATE INFOS TO DB #############################################################################
##################################################################################################

# Insert val_tuple values into DB depengind on invoked usage
def db_insup_value(target_param, val_tuple):
    cursor = connection.cursor()
    connection.commit()
    if target_param == "nsfw_mode":
        guild_id, nsfw_mode = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET nsfw_mode = %s 
                          WHERE guild_id = %s''', (nsfw_mode, guild_id,))
        if cursor.rowcount == 1:
            return True
        else:
            return False
    ##
    elif target_param == "short_reddit_timer":
        guild_id, short_reddit_timer = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET short_reddit_timer = %s 
                                  WHERE guild_id = %s''', (short_reddit_timer, guild_id,))
    ##
    elif target_param == "long_reddit_timer":
        guild_id, long_reddit_timer = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET long_reddit_timer = %s 
                                  WHERE guild_id = %s''', (long_reddit_timer, guild_id,))
    ##
    elif target_param == "censor_log_channel":
        guild_id, censor_log_channel = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET censor_log_channel = %s 
                                          WHERE guild_id = %s''', (censor_log_channel, guild_id,))
    ##
    elif target_param == "welcome_channel":
        guild_id, welcome_channel = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET welcome_channel = %s 
                                          WHERE guild_id = %s''', (welcome_channel, guild_id,))
    ##
    elif target_param == "welcome_role":
        guild_id, welcome_role = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET welcome_role = %s 
                                          WHERE guild_id = %s''', (welcome_role, guild_id,))
    ##
    elif target_param == "approb_role":
        guild_id, approb_role = val_tuple
        cursor.execute('''UPDATE servers_settings_global SET approb_role = %s 
                                          WHERE guild_id = %s''', (approb_role, guild_id,))
    ##
    elif target_param == "add_nsfw_channel":
        guild_id, guild_name, add_nsfw_channel = val_tuple
        cursor.execute('''INSERT INTO servers_nsfw_channel (guild_id, guild_name, add_nsfw_channel) 
                                  VALUES (%s, %s, %s)''', (guild_id, guild_name, add_nsfw_channel,))
    ##
    elif target_param == "add_censor_excluded_channel":
        guild_id, guild_name, add_censor_excluded_channel = val_tuple
        cursor.execute('''INSERT INTO servers_censor_excluded_channel (guild_id, guild_name, add_censor_excluded_channel) 
                                  VALUES (%s, %s, %s)''', (guild_id, guild_name, add_censor_excluded_channel,))
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
    elif target_param == "del_banned_word":
        guild_id, word = val_tuple
        cursor.execute('''DELETE FROM servers_banned_word WHERE guild_id = %s and word = %s''', (guild_id, word,))
    ##
    elif target_param == "add_emoji_role":
        guild_id, guild_name, role_name, tracked_message, emoji_id, role_id = val_tuple
        cursor.execute('''INSERT INTO servers_emoji_roles 
                                    (guild_id, guild_name, role_name, tracked_message, emoji_id, role_id) 
        VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, role_name, tracked_message, emoji_id, role_id,))

    connection.commit()
    cursor.close()


# Check if owner-admin exist, and if not, create it
def db_inspass_admin(guild_name, guild_id, user_name, user_id):
    connection.commit()
    cursor = connection.cursor()
    cursor.execute('''SELECT user_id from uwu_global_admins WHERE guild_id = %s and user_id = %s 
                    and privilege_level = 2''', (guild_id, user_id,))
    result = cursor.fetchone()
    if result:
        pass
    else:
        cursor.execute('''INSERT INTO uwu_global_admins (guild_name, guild_id, user_name, user_id, privilege_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 2,))
    connection.commit()
    cursor.close()


class DBOperations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(DBOperations(bot))
