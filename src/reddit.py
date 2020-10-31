import os

import discord
import pandas as pd
import praw
from dotenv import load_dotenv


class Reddit:
    # TODO: Add logger
    REDDIT_COLOR = 5700

    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv('REDDIT_TOKEN')
        self.CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
        self.USER_AGENT = os.getenv('REDDIT_USER_AGENT')

        self.reddit = praw.Reddit(client_id=self.CLIENT_ID, client_secret=self.TOKEN,
                                  user_agent=self.USER_AGENT)

    def get_news(self, list_subreddit, limit=1):
        # TODO: Remove useless loop

        #Check if list have subreddit
        if len(list_subreddit) == 0:
            return "Please add subreddit like that:\nreddit news"

        domains_sub = {}
        domains = {}
        domains_score = {}
        submissions_list = []

        # Loop through our selected list of subreddits
        for i in list_subreddit:
            #Check if subreddit exist
            try:
                self.reddit.subreddit(i)._fetch()
            except:
                return "'{}' subreddit does not exist.".format(i)

            # TODO: Get best item
            subreddit = self.reddit.subreddit(i)
            submissions = subreddit.top('year', limit=limit)

        for s in submissions:
            submissions_list.append(s)
            if s.id in domains_score.keys():
                domains_score[s.id] += s.score
            else:
                domains_score[s.id] = s.score

        df_score = pd.DataFrame.from_dict(domains_score, orient='index').reset_index()

        if hasattr(df_score.columns, "id") or not hasattr(df_score.columns, "score"):
            return "SubReddit found but post not found."
        else:
            df_score.columns = ['id', 'score']

        # --Grab domain for given submission ID--#
        subreddit = self.reddit.subreddit(i)
        submissions = subreddit.top('year', limit=limit)
        for s in submissions:
            if s.id in domains.keys():
                domains[s.id] = s.domain
            else:
                domains[s.id] = s.domain
        df_domain = pd.DataFrame.from_dict(domains, orient='index').reset_index()
        df_domain.columns = ['id', 'domain']

        # --Grab subreddit for given submission ID--#
        subreddit = self.reddit.subreddit(i)
        submissions = subreddit.top('year', limit=limit)
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

        # Format embed
        # TODO: Generate embed by template
        if hasattr(submissions_list[0], "url_overridden_by_dest"):
            embed = discord.Embed(title=str(submissions_list[0].title),
                                  description="Score: {}\nAuthor: {}\nReddit url: {}\nOriginal url: {}".format(
                                      submissions_list[0].score, submissions_list[0].author,
                                      submissions_list[0].shortlink,
                                      submissions_list[0].url_overridden_by_dest), color=self.REDDIT_COLOR)
        else:
            embed = discord.Embed(title=str(submissions_list[0].title),
                                  description="Score: {}\nAuthor: {}\nReddit url: {}".format(
                                      submissions_list[0].score, submissions_list[0].author,
                                      submissions_list[0].shortlink, ), color=self.REDDIT_COLOR)

        if hasattr(submissions_list[0], "selftext"):
            if submissions_list[0].selftext != '':
                embed.add_field(name="Text", value=str(submissions_list[0].selftext), inline=False)

        if submissions_list[0].url != "default" or "self":
            embed.set_image(url=str(submissions_list[0].url))

        return embed
