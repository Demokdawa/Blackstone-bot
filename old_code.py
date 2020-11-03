# !rcheck to get status of the image-serving service
@check_cog_redditscrap()
@commands.command()
async def rcheck(self, ctx):
    if rdy == 0:
        await ctx.channel.send("Je démarre gros, 2 sec 😎 ({} / {})".format(progress, len(sub_dict)))
    elif rdy == 1:
        await ctx.channel.send("Je suis la pour toi mon chou ❤")


# Decorator to check if reddit bot is ready to serve
def check_if_bot_rdy():
    async def predicate(ctx):
        if rdy == 0:
            await ctx.channel.send("Je suis encore en train de fouiller le web, patiente quelques minutes 😎 ({} / {}) "
                                   .format(progress, len(sub_dict)))

        elif rdy == 1:
            return True

    return commands.check(predicate)


sub_dict = db_get_reddit_sub_dict()  # [dict] with subs (dict key is sub)


# Get a page of top submissions in a subreddit
async def get_a_page_old(params, subreddit):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/{}/top.json'.format(subreddit), params=params) as resp:
            response = await resp.json()
            for i in response['data']['children']:
                u_name = i['data']['name']
                url_raw = i['data']['url']

                if url_raw.endswith('.jpg') or url_raw.endswith('.png'):
                    content_type = "image"
                    url = url_raw
                    reddit_poller_insert(u_name, subreddit, content_type, url)
                elif url_raw.endswith('.gifv'):
                    content_type = "gifv"
                    url = os.path.splitext(url_raw)[0] + '.gif'
                    reddit_poller_insert(u_name, subreddit, content_type, url)
                elif url_raw.endswith('.gif'):
                    content_type = "gif"
                    url = url_raw
                    reddit_poller_insert(u_name, subreddit, content_type, url)
                else:
                    content_type = "unknow"
                    url = url_raw
                    reddit_poller_insert(u_name, subreddit, content_type, url)

    return response['data']['after']


# Get a number of submissions from a subreddit (max 1000)
async def get_subreddit_old(number, subreddit):
    after = None
    params = None
    number = number
    while number != 0:
        if number > 100:
            if after is None:
                params = {'limit': 100, 't': 'all'}
            else:
                params = {'limit': 100, 'after': after, 't': 'all'}
            after = await get_a_page(params, subreddit)
            number = number - 100

        else:
            if after is None:
                params = {'limit': number, 't': 'all'}
            else:
                params = {'limit': number, 'after': after, 't': 'all'}
            await get_a_page(params, subreddit)
            number = 0
        # To respect reddit timer request
        await asyncio.sleep(2)


res = {}
for i, j, k, l, m in result:
    res[i] = [j, k, l, m]

c_dict = db_get_reddit_command_dict()  # [dict] of commands (dict key is command)
c_dict_sfw = {k: v for k, v in c_dict.items() if v[1] == 0}  # [dict] of SFW commands
c_list_sfw = [(k, v) for k, v in c_dict_sfw.items()]  # [list] of SFW commands
c_dict_nsfw = {k: v for k, v in c_dict.items() if v[1] == 1}  # [dict] of NSFW commands
c_list_nsfw = [(k, v) for k, v in c_dict_nsfw.items()]  # [list] of NSFW commands
c_list = [k for k in c_dict]  # [list] with only commands
sub_dict = db_get_reddit_sub_dict()  # [dict] with subs (dict key is sub)

