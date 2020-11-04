import aiohttp
import time
import asyncio
import asyncpraw
import os
import logging
import functools
from time import perf_counter
from discord.ext import tasks, commands
from cogs.db_operations import db_rdt_poller_insert, db_rdt_poller_clean, db_rdt_poller_sub_get, db_rdt_poller_subdata_get
from cogs.utils import precursor_restricted
from loadconfig import reddit_client_id, reddit_client_secret, reddit_user_agent, gfycat_client_id, gfycat_client_secret

# Retrieve logger
log = logging.getLogger("Poller_logs")

log.info('[COGS] RedditPoller COG loaded')

# Reddit API infos
reddit = asyncpraw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)


async def get_sub_volume(sub_size):
    if sub_size >= 10000:
        best = 1000  # Max
        return best
    elif sub_size >= 8000:
        best = sub_size / 9  # 11%
        return best
    elif sub_size >= 6000:
        best = sub_size / 9  # 11%
        return best
    elif sub_size >= 4000:
        best = sub_size / 5  # 20%
        return best
    elif sub_size >= 2000:
        best = sub_size / 3  # 33%
        return best
    elif sub_size >= 1000:
        best = sub_size / 1.5  # 66%
        return best
    elif sub_size >= 800:
        best = sub_size / 1.4  # 71%
        return best
    elif sub_size >= 600:
        best = sub_size / 1.4  # 71%
        return best
    elif sub_size >= 400:
        best = sub_size / 1.6  # 62.5%
        return best
    elif sub_size >= 200:
        best = sub_size / 1.35  # 74%
        return best
    elif sub_size >= 100:
        best = sub_size / 1.30  # 76%
        return best
    elif sub_size < 100:
        best = sub_size / 1  # 100%
        return best


# Get number of posts on a subreddit
async def get_sub_size(subreddit):
    params = {'subreddit': subreddit, 'metadata': 'True', 'size': 0}
    response = None
    while response is None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.pushshift.io/reddit/search/submission', params=params) as resp:
                    response = await resp.json(content_type=None)
        except ValueError as e:
            log.debug(e)
            pass

    data_size = await get_sub_volume(response['metadata']['total_results'])
    return data_size


# Test with asyncpraw
async def get_subreddit(number, subreddit):
    log.debug('Parsing "{}" of size "{}" ... !'.format(subreddit, number))
    sub = await reddit.subreddit(str(subreddit))
    async for submission in sub.top("all", limit=number):
        u_name = submission.name
        url_raw = submission.url

        if url_raw.endswith('.jpg') or url_raw.endswith('.png'):
            content_type = "image"
            url = url_raw
            db_rdt_poller_insert(u_name, subreddit, content_type, url)
            db_rdt_poller_clean(subreddit)  # Clean old entries

        elif url_raw.endswith('.gifv'):
            content_type = "gifv"
            url = os.path.splitext(url_raw)[0] + '.gif'
            db_rdt_poller_insert(u_name, subreddit, content_type, url)
            db_rdt_poller_clean(subreddit)  # Clean old entries

        elif url_raw.endswith('.gif'):
            content_type = "gif"
            url = url_raw
            db_rdt_poller_insert(u_name, subreddit, content_type, url)
            db_rdt_poller_clean(subreddit)  # Clean old entries

        else:
            content_type = "unknow"
            url = url_raw
            db_rdt_poller_insert(u_name, subreddit, content_type, url)
            db_rdt_poller_clean(subreddit)  # Clean old entries

    log.debug('Parsing "{}" of size "{}" Done !'.format(subreddit, number))


# Get all reddit data for the bot
async def get_reddit_data():
    # sub_list = [items[0] for items in db_rdt_poller_sub_get()]
    sub_list = [item for t in db_rdt_poller_sub_get() for item in t]
    print(sub_list)
    for sub in sub_list:
        await get_subreddit(await get_sub_size(sub), sub)


class RedditPoller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_cache.start()

    # !rsync command to refresh reddit commands and sync new subs
    @precursor_restricted()
    @commands.command(hidden=True)
    async def rsync(self, ctx):

        try:
            self.bot.reload_extension('reddit_bot')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

        curr_content_list = [items for items in db_rdt_poller_subdata_get()]
        upd_content_list = [items for items in db_rdt_poller_sub_get()]
        sub_to_sync = [item for item in upd_content_list if item not in curr_content_list]

        for sub in sub_to_sync:
            await get_subreddit(await get_sub_size(sub), sub)

        await ctx.send('**`RSYNC DONE (for subreddit/s "{}")`**'.format(sub_to_sync))

        log.debug('Rsync done (for subreddit/s "{}")'.format(sub_to_sync))

    # TASKS ##########################################################################################
    ##################################################################################################

    @tasks.loop(seconds=43200)
    async def update_cache(self):
        t1_start = perf_counter()
        await get_reddit_data()
        t1_stop = perf_counter()
        log.debug('The cache update took {} to execute'.format(t1_stop-t1_start))


def setup(bot):
    bot.add_cog(RedditPoller(bot))
