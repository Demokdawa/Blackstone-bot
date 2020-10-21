import aiohttp
import time
import asyncio
import os


async def get_a_page(params):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/dankmemes/top.json', params=params) as resp:
            response = await resp.json()
            for i in response['data']['children']:
                name = i['data']['name']
                url_raw = i['data']['url']

                if url_raw.endswith('.jpg') or url_raw.endswith('.png'):
                    content_type = "image"
                    url = url_raw
                elif url_raw.endswith('.gifv'):
                    content_type = "gifv"
                    url = os.path.splitext(url_raw)[0] + '.gif'
                elif url_raw.endswith('.gif'):
                    url = url_raw



    return response['data']['after']


async def get_subs(number):
    after = None
    params = None
    number = number
    while number != 0:
        if number > 100:
            if after is None:
                params = {'limit': 100}
            else:
                params = {'limit': 100, 'after': after}
            after = await get_a_page(params)
            number = number - 100

        else:
            if after is None:
                params = {'limit': number}
            else:
                params = {'limit': number, 'after': after}
            await get_a_page(params)
            number = 0

        time.sleep(2)

asyncio.run(get_subs(1000))