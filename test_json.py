from psaw import PushshiftAPI
import datetime as dt
import timeit
from time import perf_counter
import requests
import aiohttp
import asyncio
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)


def get_subreddit(subreddit, limit):
    api = PushshiftAPI()

    print(list(api.search_submissions(subreddit=subreddit, limit=limit)))


################################################################################


empty_list = []


async def get_a_page(params):
    global empty_list
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/dankmemes/top.json', params=params) as resp:
            response = await resp.json()

            # print(response['data']['after'])
            for i in response['data']['children']:
                url = i['data']['url']
                empty_list.append(url)
            # print(response['data']['children'][0]['data']['url'])

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
            await get_a_page({'limit': number})
            number = 0




#loop = asyncio.get_event_loop()
#loop.run_until_complete(faire_toutes_les_requetes_sans_bloquer())

t1_start = perf_counter()
get_subreddit('dankmemes', 602)
t1_stop = perf_counter()

t2_start = perf_counter()
asyncio.run(get_subs(602))
t2_stop = perf_counter()


print(len(empty_list))
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)
print("Elapsed time during the whole program in seconds:", t2_stop-t2_start)



