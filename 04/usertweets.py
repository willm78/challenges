from collections import namedtuple
import csv
import os
import json

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100


class UserTweets(object):

    def __init__(self, handle, max_id=None, count=NUM_TWEETS):
        """Get handle and optional max_id.
        Use tweepy.OAuthHandler, set_access_token and tweepy.API
        to create api interface.
        Use _get_tweets() helper to get a list of tweets.
        Save the tweets as data/<handle>.csv"""
        # ...
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        self.handle = handle
        self.max_id = max_id
        self.count = NUM_TWEETS
        self.output_file = 'data/{}.csv'.format(self.handle)
        self._tweets = list(self._get_tweets())
        self._save_tweets(self._tweets)

    def _get_tweets(self):
        """Hint: use the user_timeline() method on the api you defined in init.
        See tweepy API reference: http://docs.tweepy.org/en/v3.5.0/api.html
        Use a list comprehension / generator to filter out fields
        id_str created_at text (optionally use namedtuple)"""
        self.Tweet = namedtuple('Tweet', 'id_str created_at text')
        for status in tweepy.Cursor(self.api.user_timeline, id=self.handle, max_id=self.max_id).items(self.count):
            status = status._json
            status = map(status.get, list(self.Tweet._fields))
            status = self.Tweet._make(tweet for tweet in status)
            yield status

    def _save_tweets(self, tweets):
        """Use the csv module (csv.writer) to write out the tweets.
        If you use a namedtuple get the column names with Tweet._fields.
        Otherwise define them as: id_str created_at text
        You can use writerow for the header, writerows for the rows"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([tweet for tweet in tweets])
            
    def __len__(self):
        """See http://pybit.es/python-data-model.html"""
        return self._tweets.__len__()

    def __getitem__(self, pos):
        """See http://pybit.es/python-data-model.html"""
        return self._tweets.__getitem__(pos)


if __name__ == "__main__":

    for handle in ('pybites', 'PythonInsider', 'bbelderbos'):
        print('--- {} ---'.format(handle))
        user = UserTweets(handle)
        for tw in user[:5]:
            print(tw)
        print()
