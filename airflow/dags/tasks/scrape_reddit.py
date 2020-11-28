import logging

import praw
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(name)s : %(message)s')

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

TOP_SUBREDDITS = pd.read_csv('/task_data/top_subreddits/top_subreddits.csv')

REDDIT = praw.Reddit(client_id='3g9gcvck7Mp7sg', \
                     client_secret='W5HbQ5BHLspeybMxNtkOA5iooqM', \
                     user_agent='airflow-ml-pipeline', \
                     username='ecast229', \
                     password='Goldenpie22.')

def scrape(subreddit_name ,reddit=REDDIT):
    """ Function to scrape a subreddit
        ARGUMENTS:
            reddit: reddit API connection
            subreddit: subreddit to be scraped
    """
    try:
        subreddit = reddit.subreddit(subreddit_name)
    except ValueError:
        LOG.error("Subreddit:{} does not exist!".format(subreddit_name))

    top_subreddit = subreddit.top(limit=1000)

    LOG.info("Succsefully connected to Reddit and pulled top posts from r/{}".format(subreddit_name))

    topics_dict = { "title" : [], "score" : [], "id" : [],  "url" : [],  "comms_num" : [], "body" : [], 'gilded': []}

    for submission in top_subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["body"].append(submission.selftext)
        topics_dict["gilded"].append(submission.gilded)

    reddit_data = pd.DataFrame(topics_dict)
    #reddit_data.to_csv("/task_data/raw/raw_reddit_raw.csv", index=False)
    return reddit_data

def combine_to_one(subreddit_name_list=TOP_SUBREDDITS):
    data = subreddit_name_list.apply(lambda x: scrape(subreddit_name=str(x.item())), axis=1)
    data = pd.concat(list(data))
    data.to_csv("/task_data/raw/raw_reddit_raw.csv", index=False)
    return data

#if __name__ == '__main__':
#    posts = combine_to_one(subreddit_name_list=pd.read_csv('/home/ecast229/Predict_Reddit_Score_App/data/top_subreddits/top_subreddits.csv'))
#    print(posts)

