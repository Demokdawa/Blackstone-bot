from psaw import PushshiftAPI
import datetime as dt
import timeit
from time import perf_counter
import requests
import aiohttp
import asyncio
import pprint
import json
import cProfile
import praw
import time

pp = pprint.PrettyPrinter(indent=4)


def get_subreddit(subreddit, limit):
    api = PushshiftAPI()

    for submission in api.search_submissions(subreddit="Aww", limit=limit, sort_type='score', sort='desc'):
        print(submission.url, submission.score)


################################################################################
empty_list_1 = []

reddit = praw.Reddit(client_id="8idC4P5_L45lig", client_secret="yIuMXcbhk7_85syqBj-LF0Uyeb0", user_agent="discord:blackstones (by /u/demo-meme-bot)")


async def praw_test():
    for submission in reddit.subreddit("dankmemes").top(limit=1000):
        empty_list_1.append(submission.url)


################################################################################













#loop = asyncio.get_event_loop()
#loop.run_until_complete(faire_toutes_les_requetes_sans_bloquer())

t1_start = perf_counter()
asyncio.run(praw_test())
#get_subreddit('dankmemes', 100)
t1_stop = perf_counter()

t2_start = perf_counter()
asyncio.run(get_subs(1000))
t2_stop = perf_counter()

print("Elapsed time during the whole program-1 in seconds:", t1_stop-t1_start)
print("Elapsed time during the whole program-2 in seconds:", t2_stop-t2_start)


# DB_fields : subreddit, name, type,