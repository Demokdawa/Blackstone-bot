import praw
import time

# Initialize ##################################################################################
reddit = praw.Reddit(client_id='8idC4P5_L45lig', client_secret='yIuMXcbhk7_85syqBj-LF0Uyeb0',
                     user_agent='discord:blackstones (by /u/demo-meme-bot)')

###############################################################################################
# Config ######################################################################################
subreddit_list = ['dankmemes', 'hentaidankmemes', 'memeframe', 'cursedimages', 'FoodPorn', 'EarthPorn', 'nocontextpics',
                  'WTF', 'aww', 'SFWporn', 'yurimemes', 'yuri', 'NSFWarframe', 'yurigif', 'hentai', 'yiff', 'nekogirls',
                  'NekoHentai', 'Hentai_Gif', 'Rule34', 'ConfusedBoners', 'ecchi', 'Artistic_ecchi', 'Artistic_Hentai',
                  'ShitPostCrusaders', 'PokePorn', 'wholesomeyaoi', 'PerfectTiming', 'Creepy', 'HentaiVisualArts']

subreddit_group_hart = ['Artistic_ecchi', 'Artistic_Hentai', 'HentaiVisualArts']

big_dict = {}

rdy = 0


def sync_update_cache():
    start_time = time.time()
    global big_dict
    global rdy
    for sub in subreddit_list:
        if sub in subreddit_group_hart:
            for submission in reddit.subreddit(sub).top(limit=1000):
                if 'hart' not in big_dict:
                    big_dict['hart'] = []
                else:
                    big_dict['hart'].append(submission.url)
            print("done one !")
        else:
            for submission in reddit.subreddit(sub).top(limit=1000):
                if sub not in big_dict:
                    big_dict[sub] = []
                else:
                    big_dict[sub].append(submission.url)
            print("done one !")
    print("--- %s seconds ---" % (time.time() - start_time))
    print('Cache update done !')
    rdy = 1


sync_update_cache()
