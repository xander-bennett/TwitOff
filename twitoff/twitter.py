"""Retrieve tweets, embedding, save into database"""

import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

# This function belongs in the twitter.py file because all authorizations are here
def add_user(user):
    """Get Twitter User Data stored in our database."""
    twitter_user = TWITTER.get_user(user)
    tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')
    db_user = User(id=twitter_user.id, name=twitter_user.screen_name, newest_tweet_id=tweets[0].id)
    for tweet in tweets:
        embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)
    DB.session.add(db_user)
    DB.session.commit()
    return("Added the user: "+ str(user))
# To do: add functions later
