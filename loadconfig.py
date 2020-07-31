import json

with open('config.json') as config_file:
    data = json.load(config_file)

is_dev = data['dev']
bot_token_prod = data['bot_token_prod']
bot_token_dev = data['bot_token_dev']
db_host = data['db_host']
db_name = data['db_name']
db_user = data['db_user']
db_pass = data['db_pass']
reddit_client_id = data['reddit_client_id']
reddit_client_secret = data['reddit_client_secret']
reddit_user_agent = data['reddit_user_agent']
gfycat_client_id = data["gfycat_client_id"]
gfycat_client_secret = data["gfycat_client_secret"]
precursor_id = data["precursor_id"]
precursor_name = data["precursor_name"]
