import os

import pandas as pd
import praw
from dotenv import load_dotenv


class Reddit:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv('REDDIT_TOKEN')
        self.CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
        self.USER_AGENT = os.getenv('REDDIT_USER_AGENT')

        self.reddit = praw.Reddit(client_id=self.CLIENT_ID, client_secret=self.TOKEN,
                                  user_agent=self.USER_AGENT)

    def get_news(self, list_news):
        domains_sub = {}
        domains = {}
        domains_score = {}

        # Loop through our selected list of subreddits
        for i in list_news:
            subreddit = self.reddit.subreddit(i)
            submissions = subreddit.top('year', limit=50)

        for s in submissions:
            if s.id in domains_score.keys():
                domains_score[s.id] += s.score
            else:
                domains_score[s.id] = s.score

        df_score = pd.DataFrame.from_dict(domains_score, orient='index').reset_index()
        df_score.columns = ['id', 'score']

        # --Grab domain for given submission ID--#
        subreddit = self.reddit.subreddit(i)
        submissions = subreddit.top('year', limit=50)
        for s in submissions:
            if s.id in domains.keys():
                domains[s.id] = s.domain
            else:
                domains[s.id] = s.domain
        df_domain = pd.DataFrame.from_dict(domains, orient='index').reset_index()
        df_domain.columns = ['id', 'domain']

        # --Grab subreddit for given submission ID--#
        subreddit = self.reddit.subreddit(i)
        submissions = subreddit.top('year', limit=50)
        for s in submissions:
            if s.id in domains_sub.keys():
                domains_sub[s.id] = s.subreddit.display_name
            else:
                domains_sub[s.id] = s.subreddit.display_name
        df_subreddit = pd.DataFrame.from_dict(domains_sub, orient='index').reset_index()
        df_subreddit.columns = ['id', 'subreddit']

        df_sub_score = df_subreddit.merge(df_score, how='left', on="id")
        df_final = df_sub_score.merge(df_domain, how='left', on='id')

        # Add in submission URL using the 'id'
        df_final['url'] = ['www.reddit.com/'] + df_final['id'].astype(str)
        df_final.head()

        return str(df_final[:10])
