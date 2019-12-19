import discord
import aiohttp
import asyncio


async def test():
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://api.pushshift.io/reddit/search/submission/?subreddit=HentaiVisualArts&metadata=true&size=10') as r:
            res = await r.json()  # returns dict
            for element in res['data']:
                print(element['url'])

loop = asyncio. get_event_loop()
loop. run_until_complete(test())


