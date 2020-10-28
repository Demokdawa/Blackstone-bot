import aiohttp
import time
import asyncio
import os
from cogs.db_operations import reddit_poller_insert


async def get_a_page(params, subreddit):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/{}/top.json'.format(subreddit), params=params) as resp:
            response = await resp.json()
            for i in response['data']['children']:
                name = i['data']['name']
                url_raw = i['data']['url']

                if url_raw.endswith('.jpg') or url_raw.endswith('.png'):
                    content_type = "image"
                    url = url_raw
                    reddit_poller_insert(name, subreddit, content_type, url)
                elif url_raw.endswith('.gifv'):
                    content_type = "gifv"
                    url = os.path.splitext(url_raw)[0] + '.gif'
                    reddit_poller_insert(name, subreddit, content_type, url)
                elif url_raw.endswith('.gif'):
                    content_type = "gif"
                    url = url_raw
                    reddit_poller_insert(name, subreddit, content_type, url)
                else:
                    pass

    return response['data']['after']


async def get_subs(number, subreddit):
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

        time.sleep(2)

asyncio.run(get_subs(1000, "dankmemes"))
