import discord
import aiohttp
import asyncio

temp_list = []


async def test():
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/Rule34/top.json?limit=1000') as r:
            res = await r.json()  # returns dict
            for element in res['data']['children']:
                temp_list.append(element['data']['url'])

    print(len(temp_list))

loop = asyncio. get_event_loop()
loop. run_until_complete(test())


