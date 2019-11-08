"""Fetch embeddings and tweets for DB"""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User


TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'), config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'), config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """Add or Update a user *and* their Tweets, error if no/private user."""
    try:
        #get user info from tweepy API
        twitter_user = TWITTER.get_user(username)
        #checking unique user
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        #filtering out reply and re-tweet style tweets
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode='extended',
            since_id=db_user.newest_tweet_id)
        #if tweet is old, will skip
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            #fetch embedding and store in DB
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username,e))
        raise e
    else:
        DB.session.commit()

def update_all_users():
    """Updating all tweets for all users"""
    for user in User.query.all():
        add_or_update_user(user.name)
