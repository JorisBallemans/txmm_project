import requests, time, json, config
import pandas as pd
from urllib.error import HTTPError

def request_reddit_data(subreddit, query, count, last_post = "", delay = 0.1):
    req_url = f"https://old.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=on&sort=top&t=all"
    if last_post != "":
        req_url = f"https://old.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=on&sort=top&t=all&count={count}&after={last_post}"

    try:
        resp_text = requests.get(req_url).text
    except HTTPError:
        raise HTTPError
    time.sleep(delay)
    try:
        print("Succesfully scraped 25 posts...")
        return json.loads(resp_text)["data"]
    except:
        print("Too many requests, retrying after 10 seconds...")
        time.sleep(10)
        return request_reddit_data(subreddit, query, count, last_post, delay)

def get_reddit_posts(subreddit, query, limit = 25):
    if limit % 25 != 0:
        raise ValueError("Given limit must be a multiple of 25!")

    posts = pd.DataFrame()
    entries = []

    last_post_id = ""
    processed = 0
    while(limit >= 25):
        data = request_reddit_data(subreddit, query, processed, last_post_id) 
        entries.extend(data["children"])
        limit -= 25
        processed += 25
        last_post_id = data["after"]
        
    for entry in entries:
        new_entry = {feature: entry["data"][feature] for feature in config.FEATURES}
        posts = posts._append(new_entry, ignore_index = True)

    return posts

def main():
    queries = ["student in", "i am studying", "in university", "pursuing a degree"]
    subreddits = ["MentalHealthSupport", "mentalhealth","Anxiety","mentalillness", "selfimprovement","Depression","Offmychest",""]
    post_count = 100

    for subreddit in subreddits:
        for query in queries:
            print(f"Currently looking op posts containing '{query}' in subreddit '{subreddit}'")
            posts = get_reddit_posts(subreddit, query, post_count)
            posts.to_csv(f"{config.OUTPUT_FOLDER}{subreddit}_{query}.csv")

    # posts = get_reddit_posts("pics", "cool", 150)
    # posts.to_csv("output_test.csv")

if __name__ == "__main__":
    main()