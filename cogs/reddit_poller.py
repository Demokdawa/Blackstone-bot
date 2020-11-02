import aiohttp
import time
import asyncio
import os
import logging
import functools
from discord.ext import tasks, commands
from cogs.db_operations import reddit_poller_insert, db_get_reddit_sub_dict

# Retrieve logger
log = logging.getLogger("Poller_logs")

log.info('[COGS] RedditPoller COG loaded')


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


# Get a page of top submissions in a subreddit
async def get_a_page(params, subreddit):
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
                    pass

    return response['data']['after']


# Get a number of submissions from a subreddit (max 1000)
async def get_subreddit(number, subreddit):
    after = None
    params = None
    number = number
    while number != 0:
        if number > 100:
            if after is None:
                params = {'limit': 100}
            else:
                params = {'limit': 100, 'after': after}
            after = await get_a_page(params, subreddit)
            number = number - 100

        else:
            if after is None:
                params = {'limit': number}
            else:
                params = {'limit': number, 'after': after}
            await get_a_page(params, subreddit)
            number = 0
        # To respect reddit timer request
        await asyncio.sleep(2)


# Get all reddit data for the bot
async def get_reddit_data():
    sub_dict = db_get_reddit_sub_dict()
    for sub in sub_dict:
        if sub_dict.get(sub)[1] != 0:
            log.debug('Parsing "' + sub + '" ...')
            await get_subreddit(await get_sub_size(sub), sub)
            log.debug('Parsing "' + sub + '" Done !')


class RedditPoller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_cache.start()

    # TASKS ##########################################################################################
    ##################################################################################################

    @tasks.loop(seconds=43200)
    async def update_cache(self):
        thing = functools.partial(get_reddit_data)
        await self.bot.loop.run_in_executor(None, thing)
        # await get_reddit_data()


def setup(bot):
    bot.add_cog(RedditPoller(bot))
