import datetime
import os
import random
import sys
import time
import traceback
import logging
import exputils

from dotenv import load_dotenv

import csv

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=True)

username = "TedCruz"
filename = "data/usernames/%s_%s_%s.csv"
max_sleep_limit = 5

def get_posts(username):
    print("Starting collection of posts from user %s" % username)
    while True:
        try:
            userdetails = parler.profile(username)
            data = parler.user_feed(userdetails.get("_id"), 100, cursor="")
            feed = models.FeedSchema().load(data)
            break
        except:
            traceback.print_exc()
            time.sleep(max_sleep_limit)
    with open(filename % (username, str(datetime.date.today()), "posts"), mode="a") as posts:
        exputils.writetocsv(posts, feed.items, insert_headers=True)
    with open(filename % (username, str(datetime.date.today()), "links"), mode="a") as links:
        exputils.writetocsv(links, feed.links, insert_headers=True)
    while True:
        logging.info("is last? %s", feed.last)
        if feed.last:
            print("Exiting, all done.")
            break
        time.sleep(random.randint(1, max_sleep_limit))

        try:
            data = parler.user_feed(
                userdetails.get("_id"), 100, cursor=feed.next)
            feed = models.FeedSchema().load(data)
        except:
            traceback.print_exc()
            time.sleep(max_sleep_limit)
        finally:
            with open(filename % (username, str(datetime.date.today()), "posts"), mode="a") as posts:
                exputils.writetocsv(posts, feed.items)
            with open(filename % (username, str(datetime.date.today()), "links"), mode="a") as links:
                exputils.writetocsv(links, feed.links)


if __name__ == "__main__":
    get_posts(username=username)
