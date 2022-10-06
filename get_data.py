import json
import requests
import datetime as dt
import re
import csv

MONTHS = range(1, 13)
YEARS = range(2014,2022)
SUBREDDIT = "showerthoughts"
ENDPOINT="https://api.pushshift.io/reddit/search/submission/"

timestamps=[]

for year in YEARS:
    for month in MONTHS:
        after_timestamp = dt.datetime(year, month, 1).timestamp()

        if month==12:
            before_timestamp = dt.datetime(year+1, 1, 1).timestamp()
        else:
            before_timestamp = dt.datetime(year, month+1, 1).timestamp()

        timestamps.append((int(after_timestamp), int(before_timestamp)))

shower_thoughts=[]

for after, before in timestamps:
    payload = {
    'subreddit':SUBREDDIT, 
    'sort_type':'score',
    'fields':('title', 'selftext'),
    'after':after,
    'before':before
    }
    response = requests.get(ENDPOINT, params=payload)
    print(f"getting posts from {dt.datetime.fromtimestamp(after)} to {dt.datetime.fromtimestamp(before)}")
    for post in response.json()['data']:
        try:
            title=post['title']
            text=post['selftext']
        except: continue
        shower_thought=re.sub("\[.*?\]",'',f"{title} {text}")
        shower_thoughts.append([shower_thought])

with open('showerthoughts.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["showerthoughts"])
    writer.writerows(shower_thoughts)

print("All Done!")