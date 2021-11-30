import sys
import logging
import mysql.connector
from discord.ext import commands
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
from loadconfig import db_host, db_name, db_user, db_pass

# Variable de connection a la DB
con_pool = MySQLConnectionPool(host=db_host, database=db_name, user=db_user, password=db_pass,
                                pool_name='my_pool', pool_size=30)

# Retrieve logger
log = logging.getLogger("General_logs")

log.info('[COGS] DBOperations COG loaded')

# DB_UTILS #####################################################################################################
################################################################################################################


def init_db_con():
    db = con_pool.get_connection()
    db.commit()
    cursor = db.cursor()
    return db, cursor


def close_db_con(db, cursor, commit=False):
    if commit is True:
        db.commit()
    cursor.close()
    db.close()

# CHECK-DB #####################################################################################################
################################################################################################################


def db_uwu_check():
    testing_cursor = None
    db = con_pool.get_connection()
    try:
        if db.is_connected():
            db_info = db.get_server_info()
            log.info("Connecté a MYSQL server version " + str(db_info))
            testing_cursor = db.cursor()
            testing_cursor.execute("select database();")
            record = testing_cursor.fetchone()
            log.info("Connecté a la base de donnée: " + str(record))

    except Error as e:
        log.info("Erreur lors de la connection a MYSQL, fin du programme !" + str(e))
        sys.exit()

    finally:
        if db.is_connected():
            testing_cursor.close()
            db.close()
            log.info("Fin du test de connection MYSQL")


# Check if server data already exist
def db_check_serv_data(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT guild_id from servers_settings_global WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    close_db_con(db, cursor)  # Close DB session

    if result:
        return True
    else:
        return False


# Create server initial data (with their default values)
def db_create_serv_data(guild_name, guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''INSERT INTO servers_settings_global (guild_name, guild_id) VALUES (%s, %s)''', (guild_name, guild_id))

    close_db_con(db, cursor, commit=True)  # Close DB session


# GET GLOBAL CONFS #############################################################################################
################################################################################################################

def db_get_conf_server_all(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT nsfw_mode, short_reddit_timer, long_reddit_timer, censor_log_channel, welcome_channel, 
    welcome_role, approb_role, goulag_channel, warn_to_goulag, pmoji_user, pmoji_emoji, pmoji_message, censure_mode 
    from servers_settings_global WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    close_db_con(db, cursor)  # Close DB session

    if result:
        return result
    else:
        return None


# GET INFOS FROM DB ############################################################################################
################################################################################################################

def db_get_nsfw_channels(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT channel_id from servers_nsfw_channel WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]

    close_db_con(db, cursor)  # Close DB session

    query_list = [a_tuple[0] for a_tuple in result]  # Convert [list of tuples] to a [list]
    return query_list


def db_get_censor_words(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT word, word_replacement from servers_banned_word WHERE guild_id = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # # Result is a [list of tuples]

    close_db_con(db, cursor)  # Close DB session

    query_dict = dict(result)
    return query_dict


# Get all excluded channels that does not get censored on the server
def db_get_excl_channels(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT channel_id from servers_censor_excluded_channel WHERE guild_id = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]

    close_db_con(db, cursor)  # Close DB session

    if result:
        query_list = [a_tuple[0] for a_tuple in result]  # Convert [list of tuples] to a [list]
        return query_list
    else:
        return None


# Get all the emoji-roles on the server matching a specific message
def db_get_emoji_roles(guild_id, message_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT emoji_id, role_id from servers_emoji_roles WHERE guild_id = %s AND tracked_message = %s''',
                   (guild_id, message_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]

    close_db_con(db, cursor)  # Close DB session

    if result:
        query_dict = dict(result)
        return query_dict
    else:
        return None


# Get all the emoji-roles on the server
def db_get_server_emoji_roles(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT emoji_id, role_id, tracked_message from servers_emoji_roles WHERE guild_id = %s''', (guild_id,))
    result = cursor.fetchall()  # Result is a [list of tuples]

    close_db_con(db, cursor)  # Close DB session

    if result:
        return result
    else:
        return None


# Check the privilege of a user that try to input admin commands
def db_check_privilege(guild_id, user_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT privilege_level from servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    close_db_con(db, cursor)  # Close DB session

    if result:
        return result[0]
    else:
        return False


def db_get_admins(guild_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT user_id, privilege_level from servers_global_privileges WHERE guild_id = %s''',
                   (guild_id,))
    result = cursor.fetchall()  # Result is a [list] of [tuples]

    close_db_con(db, cursor)  # Close DB session

    if result:
        return result
    else:
        return False


# INSERT/UPDATE/DELETE INFOS TO DB #############################################################################
################################################################################################################

# Insert val_tuple values into DB depending on invoked usage
def db_insup_value(target_param, val_tuple):

    db, cursor = init_db_con()  # Init DB session

    ##
    if target_param == "nsfw_mode":
        guild_id, nsfw_mode = val_tuple
        if nsfw_mode == "reset":
            cursor.execute('''UPDATE servers_settings_global SET nsfw_mode = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET nsfw_mode = %s
                                        WHERE guild_id = %s''', (int(nsfw_mode), guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "short_reddit_timer":
        guild_id, short_reddit_timer = val_tuple
        if short_reddit_timer == "reset":
            cursor.execute('''UPDATE servers_settings_global SET short_reddit_timer = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET short_reddit_timer = %s 
                                        WHERE guild_id = %s''', (int(short_reddit_timer), guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "long_reddit_timer":
        guild_id, long_reddit_timer = val_tuple
        if long_reddit_timer == "reset":
            cursor.execute('''UPDATE servers_settings_global SET long_reddit_timer = DEFAULT 
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET long_reddit_timer = %s 
                                        WHERE guild_id = %s''', (int(long_reddit_timer), guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "censor_log_channel":
        guild_id, censor_log_channel = val_tuple
        if censor_log_channel == "reset":
            cursor.execute('''UPDATE servers_settings_global SET censor_log_channel = DEFAULT 
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET censor_log_channel = %s 
                                        WHERE guild_id = %s''', (censor_log_channel, guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "welcome_channel":
        guild_id, welcome_channel = val_tuple
        if welcome_channel == "reset":
            cursor.execute('''UPDATE servers_settings_global SET welcome_channel = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET welcome_channel = %s 
                                        WHERE guild_id = %s''', (welcome_channel, guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "welcome_role":
        guild_id, welcome_role = val_tuple
        if welcome_role == "reset":
            cursor.execute('''UPDATE servers_settings_global SET welcome_role = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET welcome_role = %s 
                                        WHERE guild_id = %s''', (welcome_role, guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "approb_role":
        guild_id, approb_role = val_tuple
        if approb_role == "reset":
            cursor.execute('''UPDATE servers_settings_global SET approb_role = DEFAULT
                                        WHERE guild_id = %s''', (guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''UPDATE servers_settings_global SET approb_role = %s 
                                        WHERE guild_id = %s''', (approb_role, guild_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "add_nsfw_channel":
        guild_id, guild_name, channel_id, channel_name = val_tuple
        cursor.execute('''SELECT channel_name from servers_nsfw_channel WHERE guild_id = %s and channel_id = %s''',
                       (guild_id, channel_id,))
        result = cursor.fetchone()
        if result:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        else:
            cursor.execute('''INSERT INTO servers_nsfw_channel (guild_id, guild_name, channel_id, channel_name) 
                                      VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, channel_id, channel_name,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "add_censor_excluded_channel":
        guild_id, guild_name, channel_id, channel_name = val_tuple
        cursor.execute('''SELECT channel_name from servers_censor_excluded_channel WHERE guild_id = %s
                        and channel_id = %s''', (guild_id, channel_id,))
        result = cursor.fetchone()
        if result:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        else:
            cursor.execute('''INSERT INTO servers_censor_excluded_channel (guild_id, guild_name, channel_id, 
                            channel_name) VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, channel_id, channel_name,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "add_banned_word":
        guild_id, guild_name, word, word_replacement = val_tuple
        cursor.execute('''SELECT word from servers_banned_word WHERE guild_id = %s and word = %s collate utf8mb4_bin''',
                       (guild_id, word,))
        result = cursor.fetchone()
        if result:
            cursor.execute('''UPDATE servers_banned_word SET word_replacement = %s 
            WHERE guild_id = %s and word = %s''', (word_replacement, guild_id, word,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''INSERT INTO servers_banned_word (guild_id, guild_name, word, word_replacement) 
                              VALUES (%s, %s, %s, %s)''', (guild_id, guild_name, word, word_replacement,))
            close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == "add_emoji_role":
        guild_id, guild_name, role_name, tracked_message, emoji_id, role_id = val_tuple
        cursor.execute('''SELECT emoji_id from servers_emoji_roles WHERE guild_id = %s and emoji_id = %s''',
                       (guild_id, emoji_id,))
        result = cursor.fetchone()
        if result:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        else:
            cursor.execute('''INSERT INTO servers_emoji_roles 
                          (guild_id, guild_name, role_name, tracked_message, emoji_id, role_id) 
            VALUES (%s, %s, %s, %s, %s, %s)''', (guild_id, guild_name, role_name, tracked_message, emoji_id, role_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session


# Delete val_tuple values from DB depending on invoked usage
def db_del_value(target_param, val_tuple):

    db, cursor = init_db_con()  # Init DB session

    ##
    if target_param == 'del_nsfw_channel':
        guild_id, channel_id = val_tuple
        cursor.execute('''DELETE FROM servers_nsfw_channel WHERE guild_id = %s and channel_id = %s''',
                       (guild_id, channel_id,))
        close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == 'del_censor_excluded_channel':
        guild_id, channel_id = val_tuple
        cursor.execute('''DELETE FROM servers_censor_excluded_channel WHERE guild_id = %s and channel_id = %s''',
                       (guild_id, channel_id,))
        close_db_con(db, cursor, commit=True)  # Close DB session
    ##
    elif target_param == 'del_banned_word':
        guild_id, word = val_tuple
        cursor.execute('''SELECT word from servers_banned_word WHERE guild_id = %s and word = %s collate utf8mb4_bin''',
                       (guild_id, word,))
        result = cursor.fetchone()
        if result:
            cursor.execute('''DELETE FROM servers_banned_word WHERE guild_id = %s and word = %s collate utf8mb4_bin''', (guild_id, word,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            close_db_con(db, cursor, commit=True)  # Close DB session
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
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False


# Check if owner-admin exist, and if not, create it
def db_inspass_admin(guild_name, guild_id, user_name, user_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT user_id from servers_global_privileges WHERE guild_id = %s and user_id = %s 
                    and privilege_level = 2''', (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    if result:
        close_db_con(db, cursor, commit=True)  # Close DB session
        pass
    else:
        cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, privilege_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 2,))
        close_db_con(db, cursor, commit=True)  # Close DB session


# Insert / Update / Delete an admin from the DB
def db_insupdel_admin(target_param, guild_name, guild_id, user_name, user_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT privilege_level FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    if target_param == 'add_uwu_admin':
        if result[0] == 1:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return True
        if result[0] == 2:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        elif result[0] == 3:
            cursor.execute('''UPDATE servers_global_privileges SET privilege_level = %s 
                            WHERE guild_id = %s and user_id = %s''', (2, guild_id, user_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, 
            privilege_level) VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 2,))
            close_db_con(db, cursor, commit=True)  # Close DB session

    elif target_param == 'del_uwu_admin':
        if result[0] == 1:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return True
        if result[0] == 2:
            cursor.execute('''DELETE FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                           (guild_id, user_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        elif result[0] == 3:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        else:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False


# Insert / Update / Delete an mod from the DB
def db_insupdel_mod(target_param, guild_name, guild_id, user_name, user_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT privilege_level FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Result is a [tuple]

    if target_param == 'add_uwu_mod':
        if result[0] == 1:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return True
        if result[0] == 3:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        elif result[0] == 2:
            cursor.execute('''UPDATE servers_global_privileges SET privilege_level = %s 
                            WHERE guild_id = %s and user_id = %s''', (3, guild_id, user_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        else:
            cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, 
            privilege_level) VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, 3,))
            close_db_con(db, cursor, commit=True)  # Close DB session

    elif target_param == 'del_uwu_mod':
        if result[0] == 1:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return True
        if result[0] == 3:
            cursor.execute('''DELETE FROM servers_global_privileges WHERE guild_id = %s and user_id = %s''',
                           (guild_id, user_id,))
            close_db_con(db, cursor, commit=True)  # Close DB session
        elif result[0] == 2:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False
        else:
            close_db_con(db, cursor, commit=True)  # Close DB session
            return False


# Add the precusor as level-1 on the server
def db_inspass_precursor(guild_name, guild_id, dev_name, dev_id):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT user_id from servers_global_privileges WHERE guild_id = %s and user_id = %s 
                        and privilege_level = 1''', (guild_id, dev_id,))
    result = cursor.fetchone()  # Result is a [tuple]
    if result:
        pass
    else:
        cursor.execute('''INSERT INTO servers_global_privileges (guild_name, guild_id, user_name, user_id, privilege_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, dev_name, dev_id, 1,))

    close_db_con(db, cursor, commit=True)  # Close DB session


# Add a warn to a user, create it if not already in DB
def db_add_warn(guild_name, guild_id, user_name, user_id, warn_level):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT user_id FROM servers_moderation_data WHERE guild_id = %s and user_id = %s''',
                   (guild_id, user_id,))
    result = cursor.fetchone()  # Return is a [tuple]

    if result:
        cursor.execute('''UPDATE servers_moderation_data SET warn_level = warn_level + %s
                        WHERE guild_id = %s and user_id = %s''', (warn_level, guild_id, user_id,))
    else:
        cursor.execute('''INSERT INTO servers_moderation_data (guild_name, guild_id, user_name, user_id, warn_level)
                        VALUES (%s, %s, %s, %s, %s)''', (guild_name, guild_id, user_name, user_id, warn_level,))

    close_db_con(db, cursor, commit=True)  # Close DB session


# REDDIT-POLLER ################################################################################################
################################################################################################################

# Return [list of tuples] of subreddits
def db_rdt_poller_sub_get():

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT subreddit_name from uwu_reddit_subreddits''')
    result = cursor.fetchall()  # Result is a [list] of [tuple]

    close_db_con(db, cursor)  # Close DB session

    return result


# Insert data from subreddit submissions
def db_rdt_poller_insert(u_name, subreddit, content_type, url):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT name FROM uwu_reddit_data WHERE name = %s''', (u_name,))
    result = cursor.fetchone()  # Return is a [tuple]

    if result:
        cursor.execute('''UPDATE uwu_reddit_data SET curr_timestamp = NULL WHERE name = %s''', (u_name,))
    else:
        cursor.execute('''INSERT INTO uwu_reddit_data (name, subreddit, content_type, url) VALUES (%s, %s, %s, %s)''',
                       (u_name, subreddit, content_type, url,))

    close_db_con(db, cursor, commit=True)  # Close DB session


# Clean old subreddit submissions
def db_rdt_poller_clean(subreddit):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''DELETE FROM uwu_reddit_data WHERE 'curr_timestamp' < CURRENT_TIMESTAMP - INTERVAL 20 MINUTE 
                                                    AND 'subreddit' = %s''', (subreddit,))

    close_db_con(db, cursor, commit=True)  # Close DB session


# Get the current subreddits that have data in db
def db_rdt_poller_subdata_get():

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''select DISTINCT subreddit from uwu_reddit_data''')
    result = cursor.fetchall()  # Result is a [list of tuples]

    # query_list = [a_tuple[0] for a_tuple in result]
    return result


# REDDIT-BOT ###################################################################################################
################################################################################################################


# Return random reddit content depending on command
def db_rdt_rand_content_get(sub_tuple):
    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT url, content_type FROM uwu_reddit_data WHERE subreddit in %s ORDER BY RAND() 
                      LIMIT 1''', (sub_tuple,))
    result = cursor.fetchone()  # Return is a [tuple]

    close_db_con(db, cursor)  # Close DB session

    return result


# Return a [list of tuples] of reddit commands
def db_rdt_cmd_data_get():

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT command_name, is_nsfw FROM uwu_reddit_commands''')
    result = cursor.fetchall()  # Result is a [list] of [tuple]

    close_db_con(db, cursor)  # Close DB session

    return result


# Return a [list of tuples] of subreddits corresponding to a command
def db_rdt_sub_translt_get(command):

    db, cursor = init_db_con()  # Init DB session

    cursor.execute('''SELECT uwu_reddit_subreddits.subreddit_name
                      FROM uwu_reddit_commands INNER JOIN uwu_reddit_subreddits 
                      WHERE uwu_reddit_commands.subreddit_group = uwu_reddit_subreddits.subreddit_group
                      AND uwu_reddit_commands.command_name = %s ''', (command,))
    result = cursor.fetchall()  # Result is a [list] of [tuple]

    close_db_con(db, cursor)  # Close DB session

    return result


class DBOperations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(DBOperations(bot))
